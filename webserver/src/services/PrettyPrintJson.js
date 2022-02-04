const PrettyPrintJson = ({data}) => (<div><pre>{JSON.stringify(data, null, 4) }</pre></div>);

export default PrettyPrintJson;