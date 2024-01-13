import { Stack } from "expo-router";
import React from "react";
import { Platform } from "react-native";

export default function ProfileLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerShown: false,
        }}
      />
      <Stack.Screen
        name="users"
        options={{
          headerShown: Platform.OS === "web",
          headerTitle: "All user roles",
          presentation: "modal",
        }}
      />
    </Stack>
  );
}
