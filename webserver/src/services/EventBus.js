/**
 * * EventBus
 *    The eventBus can share data between components.
 *
 * @method on() Creates a new event listener
 *  @param event The name of the new event listener
 *  @param callback Run a callback function after creation
 *
 * @method dispatch() Sends data to an already created event listener
 *  @param event The name of the event to send to
 *  @param data The data thats is sent. Can be anything (Object, string, etc.)
 * 
 * @method remove() Removes an existing listener
 *  @param event The name of the event listener that should be removed
 *  @param callback Run a callback function after removal of event listener
 *
 */

const eventBus = {
  on(event, callback) {
    document.addEventListener(event, (e) => callback(e.detail));
  },
  dispatch(event, data) {
    document.dispatchEvent(new CustomEvent(event, { detail: data }));
  },
  remove(event, callback) {
    document.removeEventListener(event, callback);
  },
};

export default eventBus;
