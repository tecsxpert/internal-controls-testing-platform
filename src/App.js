import { useState } from "react";

function App() {
const [input,setInput]=useState("");
const [response,setResponse]=useState("");
const [loading,setLoading]=useState(false);
const [error,setError]=useState("");

const sendToBackend=async()=>{
setLoading(true);
setError("");
setResponse("");

try{
const res=await fetch("http://127.0.0.1:8000/ai",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({text:input})
});

if(!res.ok){
throw new Error("API error");
}

const data=await res.json();
setResponse(data.response);

}catch(err){
setError("Backend not reachable / error occurred");

}finally{
setLoading(false);
}
};

return(
<div style={{
textAlign:"center",
marginTop:"80px",
fontFamily:"Arial"
}}>

<h1>AI Testing Platform</h1>

<input
value={input}
onChange={(e)=>setInput(e.target.value)}
placeholder="Enter text"
style={{
padding:"10px",
width:"300px",
borderRadius:"5px",
border:"1px solid gray"
}}
/>

<br/><br/>

<button
onClick={sendToBackend}
style={{
padding:"10px 20px",
backgroundColor:"blue",
color:"white",
border:"none",
borderRadius:"5px",
cursor:"pointer"
}}
>
Send
</button>

<br/><br/>

{loading && <p>Loading...</p>}
{response && <h3>{response}</h3>}
{error && <p style={{color:"red"}}>{error}</p>}

</div>
);
}

export default App;