import { Stack } from "expo-router";
import React from "react";
import { Platform } from "react-native";

export default function EventsLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerTitle: "All upcoming events",
          headerShown: false,
        }}
      />
      <Stack.Screen
        name="[id]"
        options={{
          headerShown: Platform.OS === "web",
          presentation: "modal",
          headerTitle: "",
        }}
      />
      <Stack.Screen
        name="create"
        options={{ headerTitle: "Create event", presentation: "modal" }}
      />
    </Stack>
  );
}
