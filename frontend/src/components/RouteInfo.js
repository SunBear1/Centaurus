import React from 'react';

function RouteInfo(props) {
    function getMinutesToDeparture(dateStr) {
        // date is a date type with in format: hh:mm (ie. 12:32)
        let date = new Date(dateStr);
        var today = new Date();

        date.setHours(date.getHours() - today.getHours());
        date.setMinutes(date.getMinutes() - today.getMinutes());

        return date.getHours() * 60 + date.getMinutes();
    }

    function getHoursAndMinutesFromDate(dateStr) {
        let date = new Date(dateStr);
        return date.toLocaleTimeString('de-DE', {
            hour: '2-digit',
            minute: '2-digit',
            });
    }

    function getLengthOfTravel(departure_time, arrival_time) {
        let departureTime = new Date(departure_time);
        let arrivalTime = new Date(arrival_time);
        
        const diffTime = Math.abs(arrivalTime - departureTime);
        const diffMinutes = Math.ceil(diffTime / (1000 * 60)); 

        return diffMinutes;
    }

    return (
        <>
            <table cellSpacing={0}>
                <thead>
                    <tr>
                        <th>Odjazd za</th>
                        <th>Linie</th>
                        <th>Czas przejazdu</th>
                    </tr>
                </thead>
                {
                    props.bestRoutes.map((routeInfo, j) => (
                        <tbody key={j} style={{ textAlign: "center" }}>
                            <tr>
                                <td>{`${getMinutesToDeparture(routeInfo.departure_time)} min`}</td>
                                <td>
                                    <div>
                                        {routeInfo.route.map((info, i) => (
                                            <div style={{display: "inline"}} key={i}><b>{`${info} `}</b></div>
                                        ))}
                                    </div>
                                    <div>
                                        {`${getHoursAndMinutesFromDate(routeInfo.departure_time)} ${getHoursAndMinutesFromDate(routeInfo.arrival_time)}`}
                                    </div>
                                </td>
                                <td>{`${getLengthOfTravel(routeInfo.departure_time, routeInfo.arrival_time)} min`}</td>
                            </tr>
                        </tbody>

                    ))
                }
            </table>
        </>
    )
}

export default RouteInfo;