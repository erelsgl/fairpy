import React, { useState } from 'react';
import axios from 'axios';
import About from "./components/About";
import Algo from "./components/Algo";
import {Button, Stack} from "@mui/material";
import SimpleAccordion from "./components/ac";

function App() {
  const [numRooms, setNumRooms] = useState('');
  const [agents, setAgents] = useState([]);
  const [totalRent, setTotalRent] = useState(0);
  const [error, setError] = useState('');

  function handleNumRoomsChange(event) {
    setNumRooms(event.target.value);
    setAgents(
      Array(Number(event.target.value))
        .fill('')
        .map(() => ({
          name: '',
          values: Array(Number(event.target.value)).fill(''),
          budget: 0,
        })),
    );
  }

  function handleTotalRentChange(event) {
    setTotalRent(event.target.value);
  }

  function handleAgentChange(event, i) {
    setAgents(
      agents.map((agent, j) => {
        if (i === j) {
          return {
            ...agent,
            name: event.target.value,
          };
        }
        return agent;
      }),
    );
  }
    const [isVisible, setIsVisible] = useState(false);

    function startVisibility() {
        if (isVisible) {
            return
        }
        setIsVisible(!isVisible);
    }
    function restVisibility(){
        if (isVisible) {
            setIsVisible(!isVisible);
        }
        return
    }
    return (
        <div>
            <About/>
            <br/>
            <div style={{padding: '5px' }}>
                <Stack spacing={2} direction="row" display= 'flex' justifyContent= 'center'>
                    <Button variant="contained" onClick={startVisibility}>Start</Button>
                    <Button variant="contained" onClick={restVisibility}>Rest</Button>
                </Stack>
                <br/>
                <div style={{padding: '10px' ,visibility: isVisible ? 'visible' : 'hidden'}}>
                    <SimpleAccordion />
                </div>
            </div>
        </div>

    )
        ;
        return agent;
      }),
    );
  }

  function handleBudgetChange(event, i) {
    setAgents(
      agents.map((agent, j) => {
        if (i === j) {
          return {
            ...agent,
            budget: event.target.value,
          };
        }
        return agent;
      }),
    );
  }

  function isDisabled() {
    return agents.some((agent) => !agent.name || agent.values.some((value) => !value)) || !totalRent;
  }

    async function handleSubmit(event) {
    event.preventDefault();
    let errorFound = false;
    agents.forEach((agent) => {
      const valuesTotal = agent.values.reduce((acc, value) => acc + parseInt(value), 0);
      if (valuesTotal !== parseInt(totalRent)) {
        setError(`Total rent does not match sum of values for ${agent.name}`);
        errorFound = true;
      }
    });
    if (!errorFound) {
      setError('');
      try {
        console.log("React: ", agents, totalRent)
        const response = await axios.post('http://localhost:5000/submit', { agents: agents , rent: totalRent});
        console.log("Flask: ", response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }

  return (
    <form>
      <label>
        Number of rooms:
        <select value={numRooms} onChange={handleNumRoomsChange}>
          {[...Array(10)].map((_, i) => (
            <option key={i}>{i + 1}</option>
          ))}
        </select>
      </label>
      <br />
      <label>
        Total Rent:
        <input type="text" value={totalRent} onChange={handleTotalRentChange} />
      </label>
      {numRooms ? (
        <table>
          <thead>
            <tr>
              <th>Agent</th>
              {Array(Number(numRooms)).fill().map((_, i) => <th key={i}>Room {i + 1}</th>)}
              <th>Budget</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent, i) => (
              <tr key={i}>
                <td>
                  <input type="text" value={agent.name} onChange={(e) => handleAgentChange(e, i)} />
                </td>
                {agent.values.map((value, j) => (
                  <td key={j}>
                    <input type="text" value={value} onChange={(e) => handleValueChange(e, i, j)} />
                  </td>
                ))}
                <td>
                  <input type="text" value={agent.budget} onChange={(e) => handleBudgetChange(e, i)} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
      <br />
      <button type="submit" onClick={handleSubmit} disabled={isDisabled()}>
        Submit
      </button>
      {error && <div>{error}</div>}
    </form>
  );
}

export default App;


