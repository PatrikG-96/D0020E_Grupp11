import { useEffect, useState } from "react";

function useEventSource(url) {
    const [data, setData] = useState(null);

    useEffect(() => {
        const source = new EventSource(url)

        source.onmessage = function logEvents(event) {
            setData(JSON.parse(event.data))
        }
      
    }, []);
    
    return data;
}

export default useEventSource;