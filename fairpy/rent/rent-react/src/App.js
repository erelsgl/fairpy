import React, {useState, useEffect} from 'react';
import axios from 'axios';
import About from "./components/About";
import Algo from "./components/Algo";
import {Button, Stack} from "@mui/material";
import SimpleAccordion from "./components/ac";

function App() {
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
}

export default App;


