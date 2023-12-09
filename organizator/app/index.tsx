import { Head } from "expo-head";
import { Stack } from "expo-router";
import { View, ScrollView } from "@gluestack-ui/themed";
import EventCard from "../components/EventCard";
import { allEventsPlaceholder } from "../utils/Placeholders";
import { getAllEvents } from "../utils/axios";

let allEvents = allEventsPlaceholder;

getAllEvents().then((response) => {
  allEvents = response.eventInformation || allEventsPlaceholder;
  console.log(allEvents);
});

export default function HomePage() {
  return (
    <>
      <Head>
        <title>Homepage</title>
      </Head>
      <ScrollView style={{ padding: "40px" }}>
        <Stack.Screen options={{ headerShown: false }} />
        <View
          style={{
            display: "flex",
            flexWrap: "wrap",
            flexDirection: "row",
            gap: "2%",
            justifyContent: "center",
          }}
        >
          {allEvents.map((event) => (
            <EventCard
              key={event.id}
              name={event.name}
              startDate={event.start_date}
              endDate={event.end_date}
              location={event.location}
              id={event.id}
              headerImage={event.header_image}
            />
          ))}
        </View>
      </ScrollView>
    </>
  );
}
