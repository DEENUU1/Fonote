import React from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/global/Layout";
import ProfileNavigationLinks from "@/components/dashboard/profile/ProfileNavigationLinks";
import HeaderText from "@/components/global/HeaderText";

export default function Home() {

	const {data: session, status} = useSession({required: true});

	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<Layout>
				<main className={"h-screen"}>{
					<>
						<HeaderText text={`Hello, ${session?.user?.email}`}/>
						<ProfileNavigationLinks/>
					</>
				}</main>
			</Layout>
		);
	}

	return <></>;
}