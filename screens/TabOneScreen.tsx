import { StyleSheet,ActivityIndicator,Switch} from 'react-native';
import React, { useState,useEffect } from 'react'

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
  const [waitTimeLeft, setWaitTimeLeft] = useState('No time');
  const [isEnabled, setIsEnabled] = useState(false);
  const [time, setTime] = useState(Date.now());

  var shuttleName = "South Campus Shuttle";
  var stop = "801 Skinker";
  var day = new Date().getDay();
  // var day = 2
  var hour = new Date().getHours();
  // var hour = 13
  var minute = new Date().getMinutes(); 
  // var minute = 30
  var htmlDropdown = '<label for="dog-names">Choose a dog name:</label><select name="dog-names" id="dog-names"><option value="rigatoni">Rigatoni</option><option value="dave">Dave</option><option value="pumpernickel">Pumpernickel</option><option value="reeses">Reeses</option></select>'
  //accept or reject
  const getData = async () => {
     try {
      const response = await fetch('http://127.0.0.1:5000/shuttle', { 
        method: 'post', 
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          shuttle: shuttleName, 
          day: JSON.stringify(day),
          hour: JSON.stringify(hour),
          minute: JSON.stringify(minute),
          stop: stop
        })
      });
      // const response = await fetch('https://reactnative.dev/movies.json');
      const json = await response.json();
      // obj = JSON.parse(json); how to copy json data?
      // why I need data
      setData(json);
      setWaitTime(json.time)
      setWaitTimeLeft(json.time_left)
      console.log(json);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }
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
  //   alert("change")
  // });

  
  const toggleSwitch = () => setIsEnabled(previousState => !previousState);

  const [selected, setSelected] = React.useState("");
  const dropdown = [
    // {key:'0', value:'Seclect shuttle',disabled:true},
    {key:'1', value:'South Campus'},
    {key:'2', value:'Campus Circulator'},
    {key:'3', value:'DeBaliviere Place Shuttle'},
    {key:'4', value:'Delmar Loop Shuttle'},
    {key:'5', value:'Lewis Collaborative Shuttle'},
    {key:'6', value:'Skinker-DeBaliviere Shuttle'},
  ]
  return (
    
    <View style={styles.container}>
      {isLoading ? <ActivityIndicator/> : (
        <View>
          <Text style = {styles.title}>Next {(stop=='Campus Circulator') ? shuttleName : 'shuttle'} at {stop}: {waitTime}</Text>
          <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
          <Text style = {styles.title}>Wait Time Left: {waitTimeLeft}</Text>
          {/* <EditScreenInfo path="/screens/TabOneScreen.tsx" /> */}
          {/* <Switch
            trackColor={{ false: "#767577", true: "#81b0ff" }}
            thumbColor={isEnabled ? "#f5dd4b" : "#f4f3f4"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch}
            value={isEnabled}
          /> */}
          
          {/* <SelectList 
            // onSelect={() => alert(selected)}
            setSelected={setSelected} 
            fontFamily='lato'
            data={dropdown}  
            search={false} 
            boxStyles={{borderRadius:0}} //override default styles
            defaultOption={{ key:'1', value:'South Campus' }}   //default selected option
          /> */}
          {/* <SelectList 
            // onSelect={() => alert(selected)}
            setSelected={setSelected} 
            fontFamily='lato'
            data={dropdown}  
            search={false} 
            boxStyles={{borderRadius:0}} //override default styles
            defaultOption={{ key:'1', value:'Mobiles' }}   //default selected option
          /> */}
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
