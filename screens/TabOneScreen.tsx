import { StyleSheet,ActivityIndicator,Switch} from 'react-native';
import React, { useState,useEffect } from 'react'
// npx expo-cli start
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { RootTabScreenProps } from '../types';

import {BrowserView, MobileView} from 'react-device-detect';
import HTMLView from 'react-native-htmlview';
import { WebView } from 'react-native-webview';
import { SelectList } from 'react-native-dropdown-select-list'

import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';

import axios from "axios";

export default function TabOneScreen({ navigation }: RootTabScreenProps<'TabOne'>) {
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [waitTime, setWaitTime] = useState('No time');
  const [waitTimeLeftH, setWaitTimeLeftH] = useState("0");
  const [waitTimeLeftM, setWaitTimeLeftM] = useState("0");
  const [selectedShuttle, setSelectedShuttle] = React.useState("South Campus Shuttle");
  const [selectedShuttleStop, setSelectedShuttleStop] = React.useState("801 Skinker");
  const [menu, setMenu] = useState(0);
  var day = new Date().getDay();
  // var day = 2
  var hour = new Date().getHours();
  // var hour = 7
  var minute = new Date().getMinutes(); 
  // var minute = 30
  
  //accept or reject
  const getData = async (loc: string | null | undefined) => {
    if(loc == null)
      loc = selectedShuttleStop
      
      try {
        const response = await fetch('http://127.0.0.1:5000/shuttle', { 
        method: 'post', 
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          shuttle: selectedShuttle, 
          day: JSON.stringify(day),
          hour: JSON.stringify(hour),
          minute: JSON.stringify(minute),
          stop: loc
        })
      });
      // const response = await fetch('https://reactnative.dev/movies.json');
      const json = await response.json();
      // obj = JSON.parse(json); how to copy json data?
      // why I need data
      // setData(json)
      setWaitTime(json.time)
      setWaitTimeLeftH(json.hour)
      setWaitTimeLeftM(json.minute)
      console.log(json);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }
  const dropdownShuttle = [
    {key:'South Campus Shuttle', value:'South Campus Shuttle'},
    {key:'Campus Circulator', value:'Campus Circulator'},
    {key:'DeBaliviere Place Shuttle', value:'DeBaliviere Place Shuttle'},
    {key:'Delmar Loop Shuttle', value:'Delmar Loop Shuttle'},
    {key:'Lewis Collaborative Shuttle', value:'Lewis Collaborative Shuttle'},
    {key:'Skinker-DeBaliviere Shuttle', value:'Skinker-DeBaliviere Shuttle'},
  ]
  const dropdownStop = [
    [
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'Rosebury  Skinker', value:'Rosebury  Skinker'},
      {key:'801 Skinker', value:'801 Skinker'},
      {key:'DeMun  Clayton', value:'DeMun  Clayton'},
      {key:'South Campus', value:'South Campus'},
      {key:'Concordia', value:'Concordia'},
    ],
    [
      {key:'S-40, Habif Health', value:'S-40, Habif Health'},
      {key:'S-40, Clocktower', value:'S-40, Clocktower'},
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'Snow Way', value:'Snow Way'},
      {key:'Millbrook Garage', value:'Millbrook Garage'},
      {key:'East End Garage', value:'East End Garage'},
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
    ],
    [
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'DeBalivere', value:'DeBalivere'},
      {key:'Pershing', value:'Pershing'},
      {key:'Belt', value:'Belt'},
      {key:'Waterman', value:'Waterman'},
      {key:'Clara', value:'Clara'},
    ],
    [
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'Lofts Apartments', value:'Lofts Apartments'},
      {key:'Westgate', value:'Westgate'},
      {key:'Washington Avenue', value:'Washington Avenue'},
      {key:'Wash Ave  Kingsland', value:'Wash Ave  Kingsland'},
      {key:'560 Music Center  ', value:'560 Music Center  '},
      {key:'S-40, Habif Health  ', value:'S-40, Habif Health  '},
      {key:'S-40, Clocktower  ', value:'S-40, Clocktower  '},
    ],
    [
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'U-City Grill', value:'U-City Grill'},
      {key:'Lewis Collab', value:'Lewis Collab'},
      {key:'Clemons  Syracuse', value:'Clemons  Syracuse'},
      {key:'Clemons  Leland', value:'Clemons  Leland'},
      {key:'Clemons  Interdrive', value:'Clemons  Interdrive'},
      {key:'Clemons  Eastgate', value:'Clemons  Eastgate'},
      {key:'Eastgate  Cates', value:'Eastgate  Cates'},
      {key:'Skinker  Delmar', value:'Skinker  Delmar'},
    ],
    [
      {key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza'},
      {key:'Skinker  Pershing', value:'Skinker  Pershing'},
      {key:'Westminster  Skinker', value:'Westminster  Skinker'},
      {key:'Westminster', value:'Westminster'},
      {key:'Rosedale  Washington', value:'Rosedale  Washington'},
      {key:'Washington  Des Peres', value:'Washington  Des Peres'},
      {key:'Kingsbury  Des Peres', value:'Kingsbury  Des Peres'},
      {key:'Des Peres  Forest Park', value:'Des Peres  Forest Park'},
    ]
  ]
  //can pending
  // const getData2 = async () => {
  //   axios({
  //     method: 'get',
  //     // responseType: 'text',
  //     // transformResponse: [v => v],
  //     // url: "/profile",
  //     // url:"http://127.0.0.1:5000/profile"
  //     url:"https://reactnative.dev/movies.json"
  //   }).then((response) => {
  //     setData(response.data)// why
  //     console.log(response.data)
  //     // resultDate = response.data.date[0] + ''
  //     // resultLocation = response.data.location[0] + ''
  //     // resultTime = response.data.time
      
  //   }).catch((err) => console.log(err)).finally(() => {
  //     setLoading(false)
  //   })
  // }
  // useEffect(() => {
  //   getData()
  //   alert("get")
  // },[]);
  useEffect(() => {
    getData(null)
  }, [isLoading,selectedShuttleStop]);
  const searchindex = ['South Campus Shuttle','Campus Circulator','DeBaliviere Place Shuttle','Delmar Loop Shuttle','Lewis Collaborative Shuttle','Skinker-DeBaliviere Shuttle']
  useEffect(() => {
    setSelectedShuttleStop("Mallinckrodt Bus Plaza")
    getData("Mallinckrodt Bus Plaza")
    const index = searchindex.indexOf(selectedShuttle)
    setMenu(index)
    
  }, [selectedShuttle]);
  
  return (
    <View style={styles.container}>
      {isLoading ? <ActivityIndicator/> : (
        <View>
          
          
          <SelectList 
            setSelected={setSelectedShuttle} 
            fontFamily='lato'
            data={dropdownShuttle}  
            search={false} 
            boxStyles={{borderRadius:0}} //override default styles
            defaultOption={{ key:'South Campus Shuttle', value:'South Campus Shuttle' }}   //default selected option
          />
          <SelectList 
            setSelected={setSelectedShuttleStop} 
            fontFamily='lato'
            data={dropdownStop[menu]}  
            search={false} 
            boxStyles={{borderRadius:0}} //override default styles
            defaultOption={{ key:'Mallinckrodt Bus Plaza', value:'Mallinckrodt Bus Plaza' }}   //default selected option
          />
          <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
          <Text style = {styles.title}>Next {selectedShuttle} at {selectedShuttleStop}: {waitTime}</Text>
          <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
          <Text style = {styles.title}>Wait Time Left: {(parseInt(waitTimeLeftH) - (new Date().getHours())) * 60 + (parseInt(waitTimeLeftM) - (new Date().getMinutes()))} minutes</Text>
        </View>
      )}
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
