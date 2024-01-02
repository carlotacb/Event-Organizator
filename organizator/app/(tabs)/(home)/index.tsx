import React, { useEffect } from "react";
import { Pressable, SafeAreaView, ScrollView, Text, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { router } from "expo-router";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { EventAllInformation } from "../../../utils/interfaces/Events";
import { getAllUpcomingEvents } from "../../../utils/api/axiosEvents";
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

const CreateButtonContainer = styled(View)`
  padding-top: 20px;
  padding-bottom: 20px;
  align-items: center;
  display: flex;
`;

const CreateButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px 30px;
  border-radius: 20px;
  gap: 10px;
  background-color: #58a659;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const CreateButtonText = styled.Text`
  font-size: 18px;
  color: white;
  font-weight: bold;
`;

export default function Home() {
  const [loading, setLoading] = React.useState(true);
  const [events, setEvents] = React.useState<EventAllInformation[]>([]);

  useEffect(() => {
    const fetchData = async () => getAllUpcomingEvents();

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.eventInformation || []);
    });
  }, []);

  return (
    <Container>
      <ScrollView contentContainerStyle={{ paddingHorizontal: 10 }}>
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
      <CreateButtonContainer>
        <CreateButton
          onPress={() => {
            router.push("/create");
          }}
        >
          <FontAwesome name="plus" size={20} color="white" />
          <CreateButtonText>Create new</CreateButtonText>
        </CreateButton>
      </CreateButtonContainer>
    </Container>
  );
}
