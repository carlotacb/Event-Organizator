import { Box, Image, VStack, Text, Heading } from "@gluestack-ui/themed";
import { MaterialCommunityIcons, Feather } from "@expo/vector-icons";
import { View } from "react-native";
import { EventCardProps } from "../utils/Interfaces";

function parseDate(dateAsString: string) {
  const date = new Date(dateAsString);
  return `${date.getDate().toString().padStart(2, "0")}-${date
    .getMonth()
    .toString()
    .padStart(2, "0")}-${date.getFullYear()} ${date
    .getHours()
    .toString()
    .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;
}

export default function EventCard(props: EventCardProps) {
  const { name, startDate, endDate, location, headerImage } = props;
  return (
    <Box
      width="$64"
      borderColor="#363636"
      borderRadius="$lg"
      borderWidth="$2"
      my="$4"
      overflow="hidden"
    >
      <Box style={{ borderBottomColor: "#E2E8F0", borderBottomWidth: 2 }}>
        <Image
          h={150}
          w="100%"
          source={{
            uri: headerImage,
          }}
        />
      </Box>
      <VStack px="$6" pt="$4" pb="$6">
        <Heading size="lg">{name}</Heading>
        <View
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: 4,
            marginTop: 10,
          }}
        >
          <MaterialCommunityIcons name="timer-sand" size={20} color="black" />
          <Text fontSize="$sm" my="$1.5">
            {parseDate(startDate)}
          </Text>
        </View>

        <View
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: 4,
          }}
        >
          <MaterialCommunityIcons
            name="timer-sand-complete"
            size={20}
            color="black"
          />{" "}
          <Text fontSize="$sm" my="$1.5">
            {parseDate(endDate)}
          </Text>
        </View>

        <View
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: 4,
          }}
        >
          <Feather name="map-pin" size={20} color="black" />
          <Text my="$1.5" fontSize="$sm" isTruncated>
            {location}
          </Text>
        </View>
      </VStack>
    </Box>
  );
}
