import React, { useEffect } from "react";
import {
  ActivityIndicator,
  Image,
  SafeAreaView,
  ScrollView,
  Text,
  View,
} from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { EventAllInformation } from "../../utils/interfaces/Events";
import getAllEvents from "../../utils/api/axiosEvents";
import Card from "../../components/Card";

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

const NoEventsContainer = styled(View)`
  padding-top: 60px;
`;

const Title = styled(Text)`
  font-size: 30px;
  font-weight: bold;
  color: black;
  text-align: center;
`;

const SubTitle = styled(Text)`
  font-size: 18px;
  color: gray;
  margin: 5px 0 20px 0;
  text-align: center;
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
          <View style={{ flex: 1, justifyContent: "center", marginTop: 30 }}>
            <ActivityIndicator size="large" />
          </View>
        ) : (
          <View style={{ justifyContent: "center" }}>
            {events.length === 0 ? (
              <NoEventsContainer>
                <Title>There are no events</Title>
                <SubTitle>
                  Come back in a few days... maybe we have news!
                </SubTitle>
                <Image
                  source={require("../../assets/noInformation.jpg")}
                  style={{ width: 280, height: 280, alignSelf: "center" }}
                />
              </NoEventsContainer>
            ) : (
              <CardsContainer>
                {events.map((event) => (
                  <Card
                    key={event.id}
                    title={event.name}
                    startDate={event.start_date}
                    endDate={event.end_date}
                    location={event.location}
                    id={event.id}
                    headerImage={event.header_image}
                  />
                ))}
              </CardsContainer>
            )}
          </View>
        )}
      </ScrollView>
    </Container>
  );
}
