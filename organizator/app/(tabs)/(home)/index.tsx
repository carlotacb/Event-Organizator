import React, { useEffect, useState } from "react";
import { Pressable, SafeAreaView, ScrollView, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { router } from "expo-router";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { useIsFocused } from "@react-navigation/native";
import { EventAllInformation } from "../../../utils/interfaces/Events";
import {
  getAllEvents,
  getAllUpcomingEvents,
} from "../../../utils/api/axiosEvents";
import Card from "../../../components/Card";
import LoadingPage from "../../../components/LodingPage";
import EmptyPage from "../../../components/EmptyPage";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import FilterButton from "../../../components/FilterButtons";

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
  margin: 20px 0;
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

const ButtonsContainer = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 5px;
  margin-top: 10px;
`;

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<EventAllInformation[]>([]);
  const [futureEvents, setFutureEvents] = useState<EventAllInformation[]>([]);
  const [allEvents, setAllEvents] = useState<EventAllInformation[]>([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const isFocused = useIsFocused();
  const [active, setActive] = useState({
    all: false,
    past: false,
    future: true,
  });

  useEffect(() => {
    const fetchData = async () => getAllUpcomingEvents();
    const fetchAllEvents = async () => getAllEvents();
    const fetchAdminFunction = async () => {
      const t = await getToken();
      return getUserRole(t);
    };

    fetchData().then((response) => {
      setLoading(false);
      setActive({ all: false, past: false, future: true });
      setEvents(response.eventInformation || []);
      setFutureEvents(response.eventInformation || []);
    });

    fetchAllEvents().then((response) => {
      setAllEvents(response.eventInformation || []);
    });

    fetchAdminFunction().then((response) => {
      setIsAdmin(response.role === UserRoles.ORGANIZER_ADMIN);
    });
  }, [isFocused]);

  return (
    <Container>
      <ScrollView contentContainerStyle={{ paddingHorizontal: 10 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <View>
            <ButtonsContainer>
              <FilterButton
                title="All"
                onPress={() => {
                  setActive({ all: true, past: false, future: false });
                  setEvents(allEvents);
                }}
                color="#040240"
                iconName="list"
                active={active.all}
              />
              <FilterButton
                title="Past"
                onPress={() => {
                  setActive({ all: false, past: true, future: false });
                  setEvents(
                    allEvents.filter(
                      (e) => e.start_date < new Date().toISOString(),
                    ),
                  );
                }}
                color="#040240"
                iconName="calendar-times-o"
                active={active.past}
              />
              <FilterButton
                title="Future"
                onPress={() => {
                  setActive({ all: false, past: false, future: true });
                  setEvents(futureEvents);
                }}
                color="#040240"
                iconName="calendar"
                active={active.future}
              />
            </ButtonsContainer>
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
          </View>
        )}
      </ScrollView>
      {isAdmin && (
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
      )}
    </Container>
  );
}
