import React, {useState, useEffect} from 'react'
import logo from './logo.svg';
import './App.css';

function App() {

  var obj = {  
    method: 'POST',
    body: JSON.stringify({
      'username' : 'patrik',
      'password' : 'woop'
    })
  }

  const [time, setTime] = useState(0)
  const [token, setToken] = useState(null)

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setTime(data.time)
    });
  }, []);

 /* useEffect(() => {
    fetch('/login?username=patrik&password=woop').then(res => res.json()).then(data => {
      setToken(data.jwt)
      window.sessionStorage.setItem("jwt", token);
    })
  })
*/
  useEffect(() => {
    fetch('/login', obj).then(res => res.json()).then(data => {
      setToken(data.jwt)
      window.sessionStorage.setItem("jwt", token);
    })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>Time is {time}</p>
        <p>Token: {token}</p>
        
      </header>
    </div>
  );
}

export default App;
