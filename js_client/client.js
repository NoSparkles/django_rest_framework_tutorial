const loginForm = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8000/api"
const contentContainer = document.getElementById('content-container')

if (loginForm){
  loginForm.addEventListener('submit', handleLogin)
}

function writeToContainer(data){
  if (contentContainer){
    contentContainer.innerHTML = "<pre>" + JSON.stringify(data, 0, 4) + '</pre>'
  }
}

function handleLogin(event){
  event.preventDefault()
  const loginEndpoint = `${baseEndpoint}/token/`
  let loginFormData = new FormData(loginForm)
  let loginObjectData = Object.fromEntries(loginFormData)
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(loginObjectData)
  }
  fetch(loginEndpoint, options)
  .then(response=>response.json())
  .then(authData=>{
    handleAuthData(authData, getProductList)
  })
}

function handleAuthData(authData, callback){
  localStorage.setItem('access', authData.access)
  localStorage.setItem('refresh', authData.refresh)
  callback(authData)
}

function getProductList(){
  const endpoint = `${baseEndpoint}/products/`
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access')}`
    }
  }
  fetch(endpoint, options)
  .then(response=>response.json())
  .then(writeToContainer)
}

function validateJWTToken() {
  const endpoint = `${baseEndpoint}/token/verify/`
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({token: localStorage.getItem('access')})
  }
  fetch(endpoint, options)
  .then(response=>response.json())
  .then(x=>{
    if (!x.ok){
      refreshToken()
      .then((newAccessToken) => {
        // You can use the new access token here or perform further actions.
        console.log('New access token:', newAccessToken);
      })
      .catch((error) => {
        // Handle any errors that occurred during token refresh.
        console.error('Token refresh error:', error);
        // You might want to perform logout or handle the error accordingly.
      });
    }
  })
}

const refreshToken = async () => {
  const getRefreshToken = () => localStorage.getItem('refresh');
  const refreshEndpoint = `${baseEndpoint}/token/refresh/`;
  const refreshToken = getRefreshToken();

  const data = {
    refresh: refreshToken,
  };

  try {
    const response = await fetch(refreshEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any additional headers required, e.g., Authorization header if needed.
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      // Handle error response, e.g., show an error message or perform logout.
      throw new Error('Token refresh failed');
    }

    const newTokens = await response.json();
    // Assuming the server returns new access and refresh tokens.
    const { access, refresh } = newTokens;

    // Save the new tokens to the client-side storage (e.g., local storage or cookies).
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);

    // Now you can use the new access token for subsequent API requests.
    // You may want to return the new access token or perform further actions here.
    return access;
  } catch (error) {
    // Handle any network errors or exceptions.
    console.error('Error refreshing token:', error);
    // You might want to perform logout or handle the error accordingly.
  }
};

validateJWTToken()