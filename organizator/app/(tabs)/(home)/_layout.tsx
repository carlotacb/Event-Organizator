import { Stack } from "expo-router";

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
    </Stack>
  );
}
