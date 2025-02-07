import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import BuildManager from './components/BuildManager';
import { AppBar, Toolbar, Button, Container } from '@material-ui/core';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Дашборд</Button>
          <Button color="inherit" component={Link} to="/build-manager">Управление сборками</Button>
        </Toolbar>
      </AppBar>
      <Container style={{ marginTop: '2rem' }}>
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route path="/build-manager" component={BuildManager} />
        </Switch>
      </Container>
    </Router>
  );
}

export default App; 