export const environment = {
  production: true,
  apiServerUrl: 'https://coffeeshop-backend.herokuapp.com', // the running FLASK api server url
  auth0: {
    url: 'kilauea.eu', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'aqpsG9A7bjLMut7HsgfQX33OALaD2fDA', // the client id generated for the auth0 app
    callbackURL: 'https://coffee-shop-full-stack.herokuapp.com', // the base url of the running ionic application. 
  }
};
