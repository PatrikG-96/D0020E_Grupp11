import axios from "axios";
import eventBus from "./EventBus";
const API_URL = "http://localhost:5000";

/**
 * ! For a more detailed overview read:
 * ! https://web.dev/push-notifications-web-push-protocol/
 *
 * @function generateEndpoint() Generates a USVString that stores an endpoint to a clients browser
 *
 *
 * @method urlBase64ToUint8Array(base64String) Encodes a base64String to Uint8 Array
 *  @param base64String 64 string public key
 *
 * @method setSubscription() subscribes the service worker to an endpoint in order to receive notifications
 *
 * @method sendToServer() Stores the created subscription and associates it with the loggin in user in the database
 *  @param sub The created subscription from setSubscription()
 */

export default function generateEndpoint() {
  function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    eventBus.dispatch("subscribeProgress", {
      message: "Encoded key complete",
      progress: 25,
    });
    return outputArray;
  }

  async function setSubscription() {
    var encodedKey = await axios
      .get(API_URL + "/subscription")
      .then((response) => {
        eventBus.dispatch("subscribeProgress", {
          message: "Generate encoded key",
          progress: 20,
        });
        return urlBase64ToUint8Array(response.data.public_key);
      });
    //"BD85L_ud7eQ_gJhg-8GoFXbCE5pHz7_fFrVOtV1W-WrdfTNpgChCA6uQdzJO-67PCJzD-nUH4ThCGauRB9byMdU";

    let swUrl = `${process.env.PUBLIC_URL}/service-worker.js`;
    navigator.serviceWorker.register(swUrl).then((response) => {
      //console.warn("response", response);
      return response.pushManager
        .getSubscription()
        .then(function (subscription) {
          eventBus.dispatch("subscribeProgress", {
            message: "Get subscription",
            progress: 30,
          });
          return response.pushManager
            .subscribe({
              userVisibleOnly: true,
              applicationServerKey: encodedKey,
            })
            .then((sub) => {
              eventBus.dispatch("subscribeProgress", {
                message: "Generate endpoint",
                progress: 50,
              });
              //console.log(JSON.stringify(response));
              subscription = JSON.stringify(sub);
              localStorage.setItem("subscription", subscription);
              sendToServer(subscription);
            });
        });
    });

    const sendToServer = async (sub) => {
      const userID = localStorage.getItem("userID");
      axios
        .post(API_URL + "/subscription", {
          sub,
          userID,
        })
        .then((response) => {
          if (response.status === 201) {
            eventBus.dispatch("subscribeProgress", {
              message: "Complete",
              sub: JSON.parse(response.data),
              complete: true,
              progress: 100,
            });
          }
        });
    };
  }
  setSubscription();
}
