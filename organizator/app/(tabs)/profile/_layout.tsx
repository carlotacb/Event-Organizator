import { Stack } from "expo-router";
import React from "react";

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
        options={{ headerTitle: "All users", presentation: "modal" }}
      />
    </Stack>
  );
}
