import { Stack } from "expo-router";

export default function NewsLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerTitle: "News",
          headerShown: false,
        }}
      />
    </Stack>
  );
}
