import { Pressable, View } from "react-native";
import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import { router } from "expo-router";
import { getToken } from "../../utils/sessionCalls";
import { getUpcomingEventsWithApplicationsInfo } from "../../utils/api/axiosEvents";
import { EventsSimpleInformationWithParticipants } from "../../utils/interfaces/Events";
import LoadingPage from "./LodingPage";
import EmptyPage from "./EmptyPage";
import CardManageEvents from "../componentsStyled/Cards/CardManageEvents";

const CardsContainer = styled(View)`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 20px 0;
`;

export default function OrganizersEventsPage() {
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<
    EventsSimpleInformationWithParticipants[]
  >([]);

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      return getUpcomingEventsWithApplicationsInfo(token || "");
    };

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.events || []);
    });
  }, []);

  return (
    <View>
      {loading ? (
        <LoadingPage />
      ) : (
        <View>
          {events.length === 0 ? (
            <EmptyPage
              title="You have no events"
              subtitle="Go back to homepage to see all our available events!"
              image={require("../../assets/empty.png")}
            />
          ) : (
            <CardsContainer>
              {events.map((event: EventsSimpleInformationWithParticipants) => (
                <Pressable
                  onPress={() => router.push(`manage/${event.event_id}`)}
                  key={event.event_id}
                >
                  <CardManageEvents
                    key={event.name}
                    title={event.name}
                    expectedAttrition={event.expected_attrition_rate}
                    maxParticipants={event.max_participants}
                    participants={event.actual_participants_count}
                  />
                </Pressable>
              ))}
            </CardsContainer>
          )}
        </View>
      )}
    </View>
  );
}
