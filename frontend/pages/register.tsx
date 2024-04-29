import Layout from "@/components/global/Layout";
import {useRouter} from 'next/router';
import HeaderText from "@/components/global/HeaderText";
import RegisterForm from "@/components/register/RegisterForm";
import {useSession} from "next-auth/react";

export default function Register() {
	const router = useRouter();
	const {data: session, status} = useSession({required: false});

	if (session) {
		return router.push('/dashboard/profile');
	}

	return (
		<Layout>
			<main>
				<>
					<HeaderText text={"Create new account"}/>
					<RegisterForm/>
				</>
			</main>
		</Layout>
	);
}
