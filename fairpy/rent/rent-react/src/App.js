import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [numRooms, setNumRooms] = useState('');
  const [agents, setAgents] = useState([]);

  function handleNumRoomsChange(event) {
    setNumRooms(event.target.value);
    setAgents(
      Array(Number(event.target.value))
        .fill('')
        .map(() => ({
          name: '',
          budgets: Array(Number(event.target.value)).fill(''),
        })),
    );
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

  function handleBudgetChange(event, i, j) {
    setAgents(
      agents.map((agent, k) => {
        if (i === k) {
          return {
            ...agent,
            budgets: agent.budgets.map((budget, l) => {
              if (j === l) {
                return event.target.value;
              }
              return budget;
            }),
          };
        }
        return agent;
      }),
    );
  }

  function isDisabled() {
    return agents.some((agent) => !agent.name || agent.budgets.some((budget) => !budget));
  }

async function handleSubmit(event) {
  event.preventDefault();
  try {
    const response = await axios.post('http://localhost:5000/submit', { agents: agents });
    console.log(response.data);
  } catch (error) {
    console.error(error);
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
      {numRooms ? (
        <table>
          <thead>
            <tr>
              <th>Agent</th>
              {Array(Number(numRooms)).fill().map((_, i) => <th key={i}>Room {i + 1}</th>)}
            </tr>
          </thead>
          <tbody>
            {agents.map((agent, i) => (
              <tr key={i}>
                <td>
                  <input type="text" value={agent.name} onChange={(e) => handleAgentChange(e, i)} />
                </td>
                {agent.budgets.map((budget, j) => (
                  <td key={j}>
                    <input type="text" value={budget} onChange={(e) => handleBudgetChange(e, i, j)} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
      <button type="submit" onClick={handleSubmit} disabled={isDisabled()}>
      Submit
      </button>
    </form>
  );
}

export default App;


