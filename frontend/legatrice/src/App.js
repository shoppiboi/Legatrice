import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React from 'react';

axios.defaults.xsrfCookieName = 'csrftoken'

class App extends React.Component {

  state = {
    currentFile: null
  };

  getLegalities = event => {
    this.setState({ currentFile: event.target.files[0] });
  };

  printFile = event => {
    event.preventDefault();
    console.log(this.state.currentFile);

    let formData = new FormData();
    formData.append('files', this.state.currentFile);

    axios
    .post('/hello/', formData,
      {headers: {'Content-Type': 'text/plain'}})
    .then((res) => console.log(res));
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
        <form>
          <div class="form-group">
            <input type="file" class="form-control-file" id="exampleFormControlFile1" onChange={this.getLegalities}></input>
          </div>
          <button class="btn btn-primary" onClick={this.printFile}>Submit</button>
        </form>
        </header>
      </div>
    )
  }
}

export default App;