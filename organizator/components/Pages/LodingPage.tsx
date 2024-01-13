import { ActivityIndicator, View } from "react-native";
import React from "react";

export default function LoadingPage() {
  return (
    <View style={{ flex: 1, justifyContent: "center", marginTop: 40 }}>
      <ActivityIndicator size="large" />
    </View>
  );
}
