import React from "react";
import { View } from "react-native";
import { Link } from "expo-router";

const Home = () => {
  return (
    <View>
      <Link href="/hackers">Go to Hackers for HackUPC</Link>
    </View>
  );
};

export default Home;
