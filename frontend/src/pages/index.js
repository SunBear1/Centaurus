import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';
import BusStopSearchBar from '../components/BusStopSearchBar';

function convertToSelectOptions(data) {
	let stops = Object.values(data)[0].stops;
	var arr = [];

	for (let index = 0; index < stops.length; index++) {
		const stop = stops[index];

		if (stop.stopName !== null && stop.stopId !== null) {
			let customLabel = `${stop.stopName} (id: ${stop.stopId})`;
			arr.push({ label: customLabel, value: stop.stopId });
		}
	}

	return arr;
}

const SearchRoute = () => {

    const [startPoint, setStartPoint] = useState({"id": undefined, "name": ""});
    const [destinationPoint, setDestinationPoint] = useState({"id": undefined, "name": ""});

    const [isStartPointChosen, setIsStartPointChosen] = useState(true);
    const [isDestinationPointChosen, setIsDestinationPointChosen] = useState(true);
	const [busStopList, setBusStopList] = useState([]);

    const navigate = useNavigate();

    
	useEffect(() => {
        function fetchData() {
            // niewiele przystankow - do testow

            // let tmpResponse =
            // {
            //     "2023-01-12": {
            //         "lastUpdate": "2023-01-12 02:51:44",
            //         "stops": [
            //             {
            //                 "stopId": 8227,
            //                 "stopCode": "04",
            //                 "stopName": "Dąbrowa Centrum",
            //                 "stopShortName": "8227",
            //                 "stopDesc": "Gdynia Dąbrowa Centrum",
            //                 "subName": "04",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 0,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.47317,
            //                 "stopLon": 18.46509,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8228,
            //                 "stopCode": "02",
            //                 "stopName": "Kameliowa",
            //                 "stopShortName": "8228",
            //                 "stopDesc": "Gdynia Kameliowa",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 0,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.47018,
            //                 "stopLon": 18.4682,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8229,
            //                 "stopCode": "02",
            //                 "stopName": "Paprykowa",
            //                 "stopShortName": "8229",
            //                 "stopDesc": "Gdynia Paprykowa",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 0,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.46784,
            //                 "stopLon": 18.46546,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8230,
            //                 "stopCode": "02",
            //                 "stopName": "Szafranowa",
            //                 "stopShortName": "8230",
            //                 "stopDesc": "Gdynia Szafranowa",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 0,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.46536,
            //                 "stopLon": 18.4602,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8231,
            //                 "stopCode": "02",
            //                 "stopName": "Leśna Polana",
            //                 "stopShortName": "8231",
            //                 "stopDesc": "Gdynia Leśna Polana (N/Ż)",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 1,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.46224,
            //                 "stopLon": 18.45337,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8234,
            //                 "stopCode": "02",
            //                 "stopName": "Centrum Nadawcze RTV",
            //                 "stopShortName": "8234",
            //                 "stopDesc": "Centrum Nadawcze RTV (N/Ż)",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 4,
            //                 "zoneName": "Żukowo",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 1,
            //                 "onDemand": 1,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.45183,
            //                 "stopLon": 18.43924,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8235,
            //                 "stopCode": "01",
            //                 "stopName": "Gdyńska",
            //                 "stopShortName": "8235",
            //                 "stopDesc": "Chwaszczyno Gdyńska (N/Ż)",
            //                 "subName": "01",
            //                 "date": "2023-01-05",
            //                 "zoneId": 4,
            //                 "zoneName": "Żukowo",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 1,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.44755,
            //                 "stopLon": 18.42786,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             },
            //             {
            //                 "stopId": 8102,
            //                 "stopCode": "02",
            //                 "stopName": "Anyżowa",
            //                 "stopShortName": "8102",
            //                 "stopDesc": "Gdynia Anyżowa",
            //                 "subName": "02",
            //                 "date": "2023-01-05",
            //                 "zoneId": 5,
            //                 "zoneName": "Gdynia",
            //                 "virtual": 0,
            //                 "nonpassenger": 0,
            //                 "depot": 0,
            //                 "ticketZoneBorder": 0,
            //                 "onDemand": 0,
            //                 "activationDate": "2023-01-12",
            //                 "stopLat": 54.47464,
            //                 "stopLon": 18.46859,
            //                 "stopUrl": "",
            //                 "locationType": null,
            //                 "parentStation": null,
            //                 "stopTimezone": "",
            //                 "wheelchairBoarding": null
            //             }
            //         ]
            //     }
            // };
            // processResponse(tmpResponse);


            // to bedzie dlugo dzialac - trzeba cachować
			fetch(`https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json`)
				.then(res => res.json())
				.then(response => processResponse(response))
				.catch(error => console.log(error));
		}
		fetchData();
    }, []);
    
    function processResponse(response) {
		setBusStopList(convertToSelectOptions(response));
	}

    async function getBestRoutes(startPoint, destinationPoint) {

        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        };

        //return fetch(`http://localhost:5000/predict?start=${startPoint}&dest=${destinationPoint}`, requestOptions)
        //let x = fetch(`http://localhost:3000/predict?start=${startPoint}&dest=${destinationPoint}`, requestOptions);
        return fetch(`http://localhost:5000/predict?start=${startPoint}&dest=${destinationPoint}`, requestOptions)
        //console.log("data", x)
        //let URL = 'http://localhost:3000/predict?start=${startPoint}&dest=${destinationPoint}'
        // fetch('http://localhost:3000/predict?start=${startPoint}&dest=${destinationPoint}')
        // .then(response=>response.json())
        // .then(data=>{ console.log("DUPA", data); })
        // fetch(URL)
        // .then(response => {
        //     let x = response.json()
        //     console.log("lol", response.json());
        //     return x;
        // })
        // .then(data => console.log(data)); // got data
        // return [
        //     {
        //         "route": [
        //             "12"
        //         ],
        //         "departure_time": "2023-01-12T20:59:00",
        //         "arrival _time": "2023-01-12T21:22:00",
        //         "routeId": 10606,
        //         "tripId": 371
        //     },
        //     {
        //         "route": [
        //             "210",
        //             "5"
        //         ],
        //         "departure_time": "2023-01-12T21:09:00",
        //         "arrival_time": "2023-01-12T21:52:00",
        //         "routeId": 10606,
        //         "tripId": 371
        //     }
        // ];
    }

    const handleStartPointChange = (userSelect) => {
        setStartPoint({ "id": userSelect.value, "name": userSelect.label });
		setIsStartPointChosen(true);
    }
    
        const handleDestinationPointChange = (userSelect) => {
        setDestinationPoint({ "id": userSelect.value, "name": userSelect.label });
		setIsDestinationPointChosen(true);
	}

    async function handleSubmit(event) {

        event.preventDefault();

        if (startPoint.id !== undefined && startPoint.name.length > 0 &&
            destinationPoint.id !== undefined && destinationPoint.name.length > 0) {
            console.log(startPoint, destinationPoint)
            getBestRoutes(startPoint.id, destinationPoint.id)
                .then(function (response) {
                    // odkomentuj i wywal returna ponizej
                    console.log("res",response)
                if (!response.ok) {
                    throw new Error("Whoops!");
                } else {
                    console.log(response.body)
                    return response.json();
                }
                })
                .then(function (data) {                  
                    navigate('/bestRoutes', { 'state': data });
                })
                .catch(function (err) {
                    alert('There was an error:' + err);
                    window.location.reload(false);
                    return false;
                });
        }
    }

    return (
        <>
            <form id='my_form' onSubmit={handleSubmit}>
                <div className='div_for_my_label'><label className='my_label'>Przystanek początkowy</label> </div>
                <BusStopSearchBar
                    busStopName={startPoint.name}
                    onSelectBusStop={handleStartPointChange}
                    isBusStopChosen={isStartPointChosen}
                    busStopList={busStopList}
                />

                <div className='div_for_my_label'><label className='my_label'>Przystanek końcowy</label> </div>
                <BusStopSearchBar
                    busStopName={destinationPoint.name}
                    onSelectBusStop={handleDestinationPointChange}
                    isBusStopChosen={isDestinationPointChosen}
                    busStopList={busStopList}
                />

                <div className='submit_input_div'><input type="submit" defaultValue="Szukaj"/></div>
            </form>
        </>
    );
};

export default SearchRoute;
