import React, { useEffect } from "react";
import { Pressable, SafeAreaView, ScrollView, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { router } from "expo-router";
import { EventAllInformation } from "../../../utils/interfaces/Events";
import { getAllEvents } from "../../../utils/api/axiosEvents";
import Card from "../../../components/Card";
import LoadingPage from "../../../components/LodingPage";
import EmptyPage from "../../../components/EmptyPage";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const CardsContainer = styled(View)`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 30px 0;
`;

export default function Home() {
  const [loading, setLoading] = React.useState(true);
  const [events, setEvents] = React.useState<EventAllInformation[]>([]);

  useEffect(() => {
    const fetchData = async () => getAllEvents();

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.eventInformation || []);
    });
  }, []);

  return (
    <Container>
      <ScrollView contentContainerStyle={{ padding: 10 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <View style={{ justifyContent: "center" }}>
            {events.length === 0 ? (
              <EmptyPage
                title="There are no events"
                subtitle="Come back in a few days... maybe we have news!"
                image={require("../../../assets/empty.png")}
              />
            ) : (
              <CardsContainer>
                {events.map((event) => (
                  <Pressable
                    onPress={() => {
                      router.push(`/${event.id}`);
                    }}
                    key={event.id}
                  >
                    <Card
                      title={event.name}
                      startDate={event.start_date}
                      endDate={event.end_date}
                      location={event.location}
                      id={event.id}
                      headerImage={event.header_image}
                    />
                  </Pressable>
                ))}
              </CardsContainer>
            )}
          </View>
        )}
      </ScrollView>
    </Container>
  );
}
