import axios from "axios";
import eventBus from "./EventBus";
const API_URL = "http://localhost:5000";

export default function swDev() {
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

    let swUrl = `${process.env.PUBLIC_URL}/sw.js`;
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
