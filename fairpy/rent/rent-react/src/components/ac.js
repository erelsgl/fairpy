import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import TextField from '@mui/material/TextField';
import {Button} from "@mui/material";
import Container from '@mui/material/Container';
import {useState} from "react";
import Grid from '@mui/material/Grid';
import * as events from "events";
import axios from "axios";


export default function SimpleAccordion() {
    const [rents, setRents] = useState(1000);
    const [roommates, setRoommates] = useState(3);
    const [bedrooms, setBedrooms] = useState(3);
    const [expanded, setExpanded] = useState(false);
    const [name, setName] = useState('')
    const [budget, setBudget] = useState('')
    const [arrValue, setArrValue] = useState({});
    const [numRooms, setNumRooms] = useState('');
    const [agents, setAgents] = useState([]);
    const handleChange = (panel) => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);

    };
    const changeRents = (event) => {
        setRents(event.target.value)
    }
    const changeRoomates = (event) => {
        setRoommates(event.target.value)
        setBedrooms(event.target.value)
        setNumRooms(event.target.value)
    }

    const handelName = (event) => {
        setName(event.target.value)
    }
    const handelBudget = (event) => {
        setBudget(event.target.value)
    }

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
            const response = await axios.post('http://localhost:5000/submit', {agents: agents});
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div>
            <Container maxWidth="sm">
                <Accordion expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
                    <AccordionSummary
                        sx={{
                            backgroundColor: '#282c34',

                        }}
                        expandIcon={<ExpandMoreIcon sx={{color: "#61dafb"}}/>}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        text-align="left"
                    >
                        <Typography sx={{color: '#61dafb'}}>THE BASICS</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>Monthly Rent</Typography>
                        <FormControl sx={{m: 1}}>
                            <InputLabel htmlFor="outlined-adornment-amount">Rent</InputLabel>
                            <OutlinedInput
                                defaultValue={rents}
                                id="rent-amount"
                                startAdornment={<InputAdornment position="start">$</InputAdornment>}
                                label="Amount"
                                onChange={changeRents}
                            />
                        </FormControl>
                        <Typography sx={{m: 2}}>Number of Roommates</Typography>
                        <TextField
                            id="roommates-number"
                            type="number"
                            InputLabelProps={{
                                shrink: true,
                            }}
                            inputProps={{min: 2, max: 20}}
                            variant="standard"
                            defaultValue={roommates}
                            onChange={changeRoomates}
                        />

                    </AccordionDetails>
                    <Button variant="contained" sx={{m: 2}} id="update-basics"
                            onClick={handleChange('panel1')}
                    >
                        Update
                    </Button>
                    <br/>
                </Accordion>

                <Accordion>
                    <AccordionSummary
                        sx={{
                            backgroundColor: '#282c34',

                        }}
                        expandIcon={<ExpandMoreIcon sx={{color: "#61dafb"}}/>}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                        text-align="left"
                    >
                        <Typography sx={{color: '#61dafb'}}>EVALUATION</Typography>
                    </AccordionSummary>
                    <AccordionDetails sx={{m: 1}}>
                        <Typography sx={{m: 2}}>
                            your values must sum to the total monthly rent: ${rents}.
                        </Typography>
                        <form>
                            <label>
                                Number of rooms:
                                <select value={numRooms} onChange={handleNumRoomsChange}>
                                    {[...Array(10)].map((_, i) => (
                                        <option key={i}>{i + 2}</option>
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
                                                <input type="text" value={agent.name}
                                                       onChange={(e) => handleAgentChange(e, i)}/>
                                            </td>
                                            {agent.budgets.map((budget, j) => (
                                                <td key={j}>
                                                    <input type="text" value={budget}
                                                           onChange={(e) => handleBudgetChange(e, i, j)}/>
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
                    </AccordionDetails>
                </Accordion>
            </Container>
        </div>
    );
}
