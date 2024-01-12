import { Stack } from "expo-router";

export default function ManageLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerShown: false,
        }}
      />
      <Stack.Screen
        name="[id]"
        options={{
          headerTitle: "All participants",
          presentation: "modal",
        }}
      />
    </Stack>
  );
}
