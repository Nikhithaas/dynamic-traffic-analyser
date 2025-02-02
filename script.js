document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    // Show the video processing section after uploading
    document.getElementById('video-section').classList.remove('hidden');

    // Fetch the uploaded files
    const file1 = document.getElementById('file1').files[0];
    const file2 = document.getElementById('file2').files[0];

    if (file1 && file2) {
        processVideos(file1, file2);
    }
});

async function processVideos(video1, video2) {
    try {
        // Copy videos to Videos folder
        await copyVideoToFolder(video1, 'junction1.mp4');
        await copyVideoToFolder(video2, 'junction2.mp4');
        
        // Wait for analysis results
        const result = await waitForAnalysis();
        
        // Extract timing data from analysis
        const timingData = {
            junction1: {
                green_time: result.junction1.timings.green_time,
                yellow_time: result.junction1.timings.yellow_time,
                density: result.junction1.density
            },
            junction2: {
                green_time: result.junction2.timings.green_time,
                yellow_time: result.junction2.timings.yellow_time,
                density: result.junction2.density
            }
        };

        // Update density displays
        document.getElementById('density1').textContent = 
            `Traffic Density: ${timingData.junction1.density} vehicles/min`;
        document.getElementById('density2').textContent = 
            `Traffic Density: ${timingData.junction2.density} vehicles/min`;

        startTrafficCycle(timingData);
    } catch (error) {
        console.error('Error processing videos:', error);
        const defaultTimingData = {
            junction1: { green_time: 30, yellow_time: 5, density: 0 },
            junction2: { green_time: 30, yellow_time: 5, density: 0 }
        };
        startTrafficCycle(defaultTimingData);
    }
}

async function copyVideoToFolder(file, filename) {
    const videosPath = 'Videos';
    const newPath = `${videosPath}/${filename}`;
    
    // Create a copy of the file in the Videos folder
    const buffer = await file.arrayBuffer();
    const newFile = new File([buffer], filename);
    
    // Use the File System Access API to save the file
    try {
        const handle = await window.showSaveFilePicker({
            suggestedName: filename,
            types: [{
                description: 'Video Files',
                accept: {'video/*': ['.mp4', '.avi', '.mov']}
            }],
        });
        const writable = await handle.createWritable();
        await writable.write(newFile);
        await writable.close();
    } catch (err) {
        console.error('Error saving file:', err);
        throw err;
    }
}

async function waitForAnalysis() {
    const maxAttempts = 30;
    let attempts = 0;
    
    while (attempts < maxAttempts) {
        try {
            const response = await fetch('analysis_result.json');
            if (response.ok) {
                return await response.json();
            }
        } catch (err) {
            // Ignore error and continue waiting
        }
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
    }
    
    throw new Error('Analysis timeout');
}

function updateTrafficLight(lightElement, state) {
    const imagePath = `images/${state}.png`;
    lightElement.src = imagePath;
    lightElement.alt = `${state.charAt(0).toUpperCase() + state.slice(1)} Light`;
    
    // Error handling for images
    lightElement.onerror = function() {
        console.error(`Failed to load ${state} light image`);
        lightElement.style.backgroundColor = state;
        lightElement.style.border = '2px solid black';
    };
}

function startTrafficCycle(timingData) {
    const light1 = document.getElementById('light1');
    const light2 = document.getElementById('light2');
    const countdown1 = document.getElementById('countdown1');
    const countdown2 = document.getElementById('countdown2');
    const state1 = document.getElementById('state1');
    const state2 = document.getElementById('state2');

    function updateCountdown(element, timeLeft) {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        element.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function updateState(stateElement, state) {
        stateElement.textContent = state.toUpperCase();
    }

    function runCycle() {
        // Junction 1 Green, Junction 2 Red
        updateTrafficLight(light1, 'green');
        updateTrafficLight(light2, 'red');
        updateState(state1, 'green');
        updateState(state2, 'red');
        
        let timeLeft1 = timingData.junction1.green_time;
        let timeLeft2 = timingData.junction1.green_time;
        
        const greenInterval1 = setInterval(() => {
            updateCountdown(countdown1, timeLeft1);
            updateCountdown(countdown2, timeLeft2);
            timeLeft1--;
            timeLeft2--;
            
            if (timeLeft1 < 0) {
                clearInterval(greenInterval1);
                transitionYellow();
            }
        }, 1000);

        function transitionYellow() {
            // Both junctions show yellow
            updateTrafficLight(light1, 'yellow');
            updateTrafficLight(light2, 'yellow');
            updateState(state1, 'yellow');
            updateState(state2, 'yellow');
            
            timeLeft1 = timingData.junction1.yellow_time;
            timeLeft2 = timingData.junction1.yellow_time;
            
            const yellowInterval = setInterval(() => {
                updateCountdown(countdown1, timeLeft1);
                updateCountdown(countdown2, timeLeft2);
                timeLeft1--;
                timeLeft2--;
                
                if (timeLeft1 < 0) {
                    clearInterval(yellowInterval);
                    startJunction2Cycle();
                }
            }, 1000);
        }

        function startJunction2Cycle() {
            updateTrafficLight(light1, 'red');
            updateTrafficLight(light2, 'green');
            updateState(state1, 'red');
            updateState(state2, 'green');
            
            timeLeft1 = timingData.junction2.green_time;
            timeLeft2 = timingData.junction2.green_time;
            
            const greenInterval2 = setInterval(() => {
                updateCountdown(countdown1, timeLeft1);
                updateCountdown(countdown2, timeLeft2);
                timeLeft1--;
                timeLeft2--;
                
                if (timeLeft2 < 0) {
                    clearInterval(greenInterval2);
                    transitionYellow2();
                }
            }, 1000);
        }

        function transitionYellow2() {
            // Both junctions show yellow again
            updateTrafficLight(light1, 'yellow');
            updateTrafficLight(light2, 'yellow');
            updateState(state1, 'yellow');
            updateState(state2, 'yellow');
            
            timeLeft1 = timingData.junction2.yellow_time;
            timeLeft2 = timingData.junction2.yellow_time;
            
            const yellowInterval2 = setInterval(() => {
                updateCountdown(countdown1, timeLeft1);
                updateCountdown(countdown2, timeLeft2);
                timeLeft1--;
                timeLeft2--;
                
                if (timeLeft2 < 0) {
                    clearInterval(yellowInterval2);
                    runCycle(); // Start the cycle again
                }
            }, 1000);
        }
    }

    // Start the traffic light cycle
    runCycle();
}
