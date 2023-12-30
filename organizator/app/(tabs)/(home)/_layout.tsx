import { Stack } from "expo-router";
import React from "react";

export default function EventsLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerTitle: "All upcoming events",
        }}
      />
      <Stack.Screen
        name="[id]"
        options={{ headerShown: false, presentation: "modal" }}
      />
      <Stack.Screen
        name="create"
        options={{ headerTitle: "Create event", presentation: "modal" }}
      />
    </Stack>
  );
}
