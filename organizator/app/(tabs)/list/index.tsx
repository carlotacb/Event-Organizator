import React from "react";
import { View } from "react-native";
import { Link } from "expo-router";

const ListPage = () => {
  return (
    <View>
      <Link href="/list/1">News 1</Link>
      <Link href="/list/2">News 2</Link>
      <Link href="/list/3">News 3</Link>
    </View>
  );
};

export default ListPage;
