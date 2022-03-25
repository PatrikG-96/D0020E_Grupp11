import axios from "axios";

const API_URL = "http://127.0.0.1:2000";

/**
 * * Methods for user creation and authentication
 
 * @method signup()
 *  @param username 
 *  @param password  
 *  @param signupCode a code stored on the server side in order to block unwanted singups
 *
 * @method login() Logs in the user and stores the username and userID in the localStorage
 *  @param username 
 *  @param password
 *
 * @method logout() Removes all the information on the user from localStorage
 * 
 * @method getCurrentUser() function for retreiving the stored (logged in) user
 */
const signup = (username, password, signupCode) => {
  return axios
    .post(API_URL + "/auth/signup", {
      username,
      password,
      signupCode,
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const login = (username, password) => {
  return axios
    .post(API_URL + "/auth/login", {
      username,
      password,
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data.accessToken));
      }
      if (response.data.userID) {
        localStorage.setItem("userID", response.data.userID);
      }
      // axios
      //   .get(API_URL + "/subscription", {
      //     params: { userID: response.data.userID },
      //   })
      //   .then((sub) => {
      //     const endpoint = JSON.parse(sub.data.endpoint);
      //     localStorage.setItem("subscription", JSON.stringify(endpoint));
      //   });
      return response.data;
    });
};

const logout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("userID");
  localStorage.removeItem("subscription");
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"));
};

const AuthService = {
  signup,
  login,
  logout,
  getCurrentUser,
};

export default AuthService;
