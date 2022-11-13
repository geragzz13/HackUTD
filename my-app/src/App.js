import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from 'react';
import axios from 'axios';

const fs = eval(require("fs"));

function RetreiveData(FileName){
  const Content= fs.readFile(FileName, {encoding: "utf-8", flag: "r"}, function(Error, Data){
    if (Error){
      console.log(Error);
    }
    else{
      const ContentArray= Content.split(/\r?\n/);

      var BaseMap= [];
      for (CurrentLine of ContentArray){
        var Commas= 0;
        var CurrentMap= new Map();
        var Word= "";

        for (var Index= 0; Index < CurrentLine.length; Index++){
          var Character= CurrentLine[Index];

          if (Character == ','){
            Commas+= 1;
          }
          if (Commas == 1){
            CurrentMap.set("BIT_DEPTH", Word);
            Word= "";
          }
          else if (Commas == 2){
            CurrentMap.set("RATE_OF_PENETRATION", Word);
            Word= "";
          }
          else if (Commas == 3){
            CurrentMap.set("HOOK_LOAD", Word);
            Word= "";
          }
          else if (Commas == 4){
            CurrentMap.set("DIFFERENTIAL_PRESSURE", Word);
            Word= "";
          }
          else if (Commas == 5){
            CurrentMap.set("WEIGHT_ON_BIT", Word);
            Word= "";
          }
          else if (Commas == 6){
            CurrentMap.set("DRILL_BIT_ID", Word);
            Word= "";
          }
          else if (Index == CurrentLine.length - 1){
            CurrentMap.set("DRILL_BIT_ID", Word);
            Word= "";
          }
          else{
            Word+= Character;
          }
        }
        Commas= 0;
        
      }
      BaseMap.push(CurrentMap);
      console.log(ContentArray);
    }
  });
}

function App() {
  for(var Number= 1; Number <= 20; Number++){
    RetreiveData("./Asteroids/Asteroid " + Number + ".csv");
  }
  //RetreiveData("../Asteroids/Asteroid 1.csv");

  const [GetMessage, SetGetMessage]= useState({});

  useEffect(() => {
    axios.get("http://localhost:5000/flask/main").then
  })

  return (
    <h1>Hello World</h1>
  );
}

export default App;
