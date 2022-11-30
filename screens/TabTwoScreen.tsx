import { StyleSheet } from 'react-native';

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';

import {BrowserView, MobileView} from 'react-device-detect';
import HTMLView from 'react-native-htmlview';
import { WebView } from 'react-native-webview';

export default function TabTwoScreen() {


  const url = 'https://parking.wustl.edu/campus-shuttle-system/'
  const urlWeb = '<a href=' + url + '>Washu shuttle website</a>'
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Thank you</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      {/* <BrowserView>
        <HTMLView
          value={urlWeb}
        />
      </BrowserView> */}
      {/* <MobileView>
        <WebView
          originWhitelist={['*']}
          source={{ html: '<h1>Hello world</h1>' }}
        />
      </MobileView> */}
    </View>
  );
}

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
