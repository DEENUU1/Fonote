import {signIn, useSession} from "next-auth/react";
import {Box, Button, Spinner, Text, VStack} from "@chakra-ui/react";

export default function Home() {

  const {data: session, status} = useSession();

  if (status == "loading") {
    return <Spinner size="lg"/>;
  }

  return (
    <Box m={8}>
      <VStack>
        <Text>
          {session ? `Hello, ${session.user.username}` : "You are not logged in"}
        </Text>

        <Button colorScheme="blue" onClick={() => signIn(undefined, {callbackUrl: "/profile"})}>
          Login
        </Button>

      </VStack>
    </Box>
  );
}