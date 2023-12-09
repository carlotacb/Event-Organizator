import { Box, Image, VStack, Text, Heading, Link } from "@gluestack-ui/themed";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faMugSaucer } from "@fortawesome/free-solid-svg-icons/faMugSaucer";

import { EventCardProps } from "../utils/Interfaces";

export default function EventCard(props: EventCardProps) {
  const { name, startDate, endDate, location, headerImage } = props;
  return (
    <Box
      maxWidth="$64"
      borderColor="$borderLight200"
      borderRadius="$lg"
      borderWidth="$1"
      my="$4"
      overflow="hidden"
    >
      <Box>
        <Image
          h={150}
          w="100%"
          source={{
            uri: headerImage,
          }}
        />
      </Box>
      <VStack px="$6" pt="$4" pb="$6">
        <Heading size="md">{name}</Heading>
        <FontAwesomeIcon icon={faMugSaucer} />q
        <Text fontSize="$sm" my="$1.5">
          {startDate}
        </Text>
        <Text my="$1.5" fontSize="$xs" isTruncated>
          {location}
        </Text>
        <Link href="https://gluestack.io/" isExternal>
          <Text fontSize="$sm" color="$pink600">
            Find out more
          </Text>
        </Link>
      </VStack>
    </Box>
  );
}
