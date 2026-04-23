import React,{useState}from"react";
function App(){
const[input,setInput]=useState("");
const[response,setResponse]=useState("");
const sendToBackend=async()=>{
try{
const res=await fetch("http://127.0.0.1:8000/ai",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({text:input})
});
const data=await res.json();
setResponse(data.response);
}catch{
setResponse("Error connecting to backend");
}
};
return(
<div style={{textAlign:"center",marginTop:"50px"}}>
<h1>AI Testing Platform</h1>
<input value={input} onChange={(e)=>setInput(e.target.value)} placeholder="Enter text"/>
<br/><br/>
<button onClick={sendToBackend}>Send</button>
<h3>{response}</h3>
</div>
);
}
export default App;