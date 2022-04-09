import React, { useState, useEffect ,useRef} from 'react';

const SearchPage = (props) => {

  const [userInput, setInput] = useState('');
  const [newsListDefault, setnewsListDefault] = useState();
  const [newsList, setnewsList] = useState([]);
  const [suggestion, setSuggestion] = useState();

  const fetchData = async () => {
    return await fetch('http://127.0.0.1:8000/latest')
      .then(response => response.json())
      .then(data => {
         setnewsList(data) 
         setnewsListDefault(data)
       });}

const Search = async (e) =>{
  e.preventDefault();
      await fetch('http://127.0.0.1:8000/news/' + userInput)
      .then(response => response.json())
      .then(data => {
          if(data["results"] == null){
            alert("Unsupported search")
          }
          setnewsList(data["results"]);
          setnewsListDefault(data["results"]);
          console.log(data["results"])
      })
}
const toTitleCase = (str) => {
  return str.replace(
    /\w\S*/g,
    function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

const updateUserInput = async (userInput) => {
  let matches = []
  if(userInput.length > 0){

      matches = newsListDefault.filter(news => {
        return news.title.toLowerCase().includes(userInput.toLowerCase())
      })
      console.log(matches)
      setSuggestion(matches)
  }
  setInput(userInput)
}

  useEffect( () => {fetchData()},[]);
  const BarStyling = {width:"20rem",background:"#F2F1F9", border:"none", padding:"0.5rem"};
  const BtnStyling = {padding:"0.5rem"}
  return (
    <>
      <h1>OneNews</h1>

    <div >
    <input 
     style={BarStyling}
     key="random1"
     value={userInput}
     placeholder={"search news"}
     onChange={(e) => updateUserInput(e.target.value)}
    />
    {/* {suggestion && suggestion.map((suggestion, i) =>
    <div key={i} className="col-md-12 justify-content-md-center" >
      {toTitleCase(suggestion.title)}
    </div> */}
    
{/*     
    )} */}
    <button style={BtnStyling} onClick={(e) => {Search(e)}}>search</button>

    </div>
    <table>
    
    {newsList.map((data,index) => {
        if (data) {
          return (
            <div key={data.title}>
              <h1>{toTitleCase(data.title)}</h1>
              <p>Category: {toTitleCase(data.category)}</p>
              <p>Author: {toTitleCase(data.author)}</p>
              <p>Location: {toTitleCase(data.location)} </p>
              <p>Date: {data.created_time}</p>
              <p>{data.content}</p>
              <img src={data.image} width="320" height="160"></img>

	    </div>	
    	   )	
    	 }
    	 return null
    }) }
    </table>
        </>
   );
}

export default SearchPage

