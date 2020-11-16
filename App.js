import React, { useState } from "react";
import { StyleSheet, View, Dimensions, Animated } from "react-native";
import { Input, Header, Button, Icon } from "./components";

const { height } = Dimensions.get("screen");

export default function App() {
  const [alignment, setAlignment] = useState(new Animated.Value(0));

  const toDocumentsPage = () => {
    Animated.timing(alignment, {
      toValue: 1,
      duration: 1500,
      useNativeDriver: false,
    }).start();
  };

  const backToMainComponent = () => {
    Animated.timing(alignment, {
      toValue: 0,
      duration: 1500,
      useNativeDriver: false,
    }).start();
  };


  const heightIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [height, 0],
  });

  const opacityIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [1, 0],
  });

  const documentPageOpacityIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 1],
  });

  const documentPageHeightIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [0, height],
  });

  const mainContainerStyle = {
    height: heightIntropolate,
    opacity: opacityIntropolate,
  };

  const documentContainerStyle = {
    height: documentPageHeightIntropolate,
    opacity: documentPageOpacityIntropolate,
  };

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.mainContainer, mainContainerStyle]}>
        <View style={{ width: "100%" }}>
          <Header title="Registrate" subTitle="Llene los siguientes campos" />
        </View>
        <View>
          <Input icon="md-person" placeholder="Nombre de usuario" />
          <Input icon="md-mail" placeholder="Email" />
          <Input icon="ios-lock" placeholder="Contraseña" />
          <Input icon="ios-lock" placeholder="Confirme su Contraseña" />
        </View>
        <Button onPress={() => toDocumentsPage()} title="Registrar" />
      </Animated.View>
      <Animated.View style={[styles.mainContainer, documentContainerStyle]}>
        
        <View style={{ width: "80%" }}>
          <Header
            title="Registro finalizado con exito"
            subTitle="Gracias por registrarse"
          />
        </View>
        <Button onPress={() => backToMainComponent()} title="Iniciar sesion" />
      </Animated.View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  mainContainer: {
    backgroundColor: "#4ba",
    alignItems: "center",
    justifyContent: "center",
  },
});
