import React from "react";
import { Text, View } from "react-native";
import { useLocalSearchParams } from "expo-router";

const NewsDetailsPage = () => {
  const { id } = useLocalSearchParams();

  return (
    <View>
      <Text>My News: {id}</Text>
    </View>
  );
};

export default NewsDetailsPage;
