import React, {useState} from 'react';
import axios from 'axios';
import './about.css'
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Container from '@mui/material/Container';

function App() {
    const [numRooms, setNumRooms] = useState('');
    const [agents, setAgents] = useState([]);
    const [totalRent, setTotalRent] = useState(0);
    const [error, setError] = useState('');
    const [results, setResults] = useState(null);

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

    function handleValueChange(event, i, j) {
        setAgents(
            agents.map((agent, k) => {
                if (i === k) {
                    return {
                        ...agent,
                        values: agent.values.map((value, l) => {
                            if (j === l) {
                                return event.target.value;
                            }
                            return value;
                        }),
                    };
                }
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
                const response = await axios.post('http://localhost:5000/submit', {agents: agents, rent: totalRent});
                console.log("Flask: ", response.data);
                setResults(response.data);
                setExpanded('panel1')
            } catch (error) {
                console.error(error);
            }
        }
    }

    const [expanded, setExpanded] = useState(false);
    const handleChange = (panel) => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);

    };
    return (
        <div className="About">
            <h1>Fair Rent Division on a Budget</h1>
            <Container maxWidth="sm">
                <Accordion>
                    <AccordionSummary
                        sx={{
                            backgroundColor: '#282c34', color: "#61dafb"

                        }}
                        expandIcon={<ExpandMoreIcon sx={{color: "#61dafb"}}/>}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        text-align="center"
                    >
                        <Typography>About</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            "Fair Rent Division on a Budget" by Procaccia, A., Velez, R., & Yu, D. (2018),
                            https://doi.org/10.1609/aaai.v32i1.11465 .<br/>
                            The algorithm calculates Optimal envy-free allocation subject to budget constraints, or in
                            simple
                            words,
                            calculates a fair rent division under budget constraints.
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </Container>
            <Container maxWidth="sm">
                <Accordion>
                    <AccordionSummary
                        sx={{
                            backgroundColor: '#282c34', color: "#61dafb"

                        }}
                        expandIcon={<ExpandMoreIcon sx={{color: "#61dafb"}}/>}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        text-align="center"
                    >
                        <Typography>manual</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            Select the number of rooms, enter the total rent.<br/>
                            Enter the names of roommates and enter the budget of each .<br/>
                            Enter the evaluation of each room so that the total equals rent.<br/>
                            For the end click on submit for result.
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </Container>
            <br/>
            <h3>START</h3>
            <form>
                <label>
                    Number of rooms:
                    <select value={numRooms} onChange={handleNumRoomsChange}>
                        {[...Array(10)].map((_, i) => (
                            <option key={i}>{i + 2}</option>
                        ))}
                    </select>
                </label>
                <br/>
                <br/>
                <label>
                    Total Rent:
                    <input type="text" value={totalRent} onChange={handleTotalRentChange}/>
                </label>
                <br/>
                <br/>
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
                                    <input type="text" value={agent.name} onChange={(e) => handleAgentChange(e, i)}/>
                                </td>
                                {agent.values.map((value, j) => (
                                    <td key={j}>
                                        <input type="text" value={value} onChange={(e) => handleValueChange(e, i, j)}/>
                                    </td>
                                ))}
                                <td>
                                    <input type="text" value={agent.budget} onChange={(e) => handleBudgetChange(e, i)}/>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                ) : null}
                <br/>
                {error ? <p style={{color: 'red'}}>{error}</p> : null}
                <button type="submit" onClick={handleSubmit} disabled={isDisabled()}>
                    Submit
                </button>
            </form>
            <Container maxWidth="sm">
                <Accordion expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
                    <AccordionSummary
                        sx={{
                            backgroundColor: '#282c34', color: "#61dafb"

                        }}
                        expandIcon={<ExpandMoreIcon sx={{color: "#61dafb"}}/>}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        text-align="center"
                    >
                        <Typography>Result</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>
                            <div>
                                {results && results != "no solution" ? (
                                    <table>
                                        <thead>
                                        <tr>
                                            <th>Agent</th>
                                            <th>Room</th>
                                            <th>Value</th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {results[0].map((result, i) => (
                                            <tr key={result[0]}>
                                                <td>{result[0]}</td>
                                                <td>{result[1]}</td>
                                                <td>{results[1][i][1]}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                ) : results == "no solution" ? <p>No solution</p> : null}
                            </div>
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </Container>
        </div>
    );
}

export default App;


