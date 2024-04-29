import {Button} from "@chakra-ui/react";
import {signIn} from "next-auth/react";
import React, {useState} from "react";
import {useRouter} from "next/router";
import {toast} from "react-toastify";
import Link from "next/link";


export default function RegisterForm() {
	const [formData, setFormData] = useState({ // State to hold form data
		email: "",
		password1: "",
		password2: ""
	});
	const router = useRouter();

	const handleChange = (e: any) => {
		const {name, value} = e.target;
		setFormData(prevState => ({
			...prevState,
			[name]: value
		}));
	};

	const handleSubmit = async (e: any) => {
		e.preventDefault();

		try {
			const response = await fetch(process.env.API_URL + 'auth/register/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(formData)
			});

			const res = await response.json();

			if (response.ok) {
				router.push("/dashboard/profile");
			} else {
				const firstErrorKey = Object.keys(res)[0];
				const firstErrorMessage = res[firstErrorKey][0];
				toast.error(firstErrorMessage);
			}
		} catch (error) {
			toast.error("Error while creating user. Please try again.");
		}
	};
	return (

		<>
			<div className="flex flex-col justify-center font-[sans-serif] text-[#333] sm:h-screen p-4">
				<div className="max-w-md w-full mx-auto border border-gray-300 rounded-md p-6">
					<form onSubmit={handleSubmit}>
						<div className="space-y-6">
							<div>
								<label className="text-sm mb-2 block">Email</label>
								<input required={true} name="email" type="text" value={formData.email} onChange={handleChange}
											 className="bg-white border border-gray-300 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
											 placeholder="Enter email"/>
							</div>
							<div>
								<label className="text-sm mb-2 block">Password</label>
								<input required={true} name="password1" type="password" value={formData.password1}
											 onChange={handleChange}
											 className="bg-white border border-gray-300 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
											 placeholder="Enter password"/>
							</div>
							<div>
								<label className="text-sm mb-2 block">Confirm Password</label>
								<input required={true} name="password2" type="password" value={formData.password2}
											 onChange={handleChange}
											 className="bg-white border border-gray-300 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
											 placeholder="Enter confirm password"/>
							</div>
							<div className="flex items-center">
								<input required={true} id="remember-me" name="remember-me" type="checkbox"
											 className="h-4 w-4 shrink-0 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"/>
								<label htmlFor="remember-me" className="ml-3 block text-sm">
									I accept the <Link href="/" className="text-blue-600 font-semibold hover:underline ml-1">Terms and
									Conditions</Link>
								</label>
							</div>
						</div>

						<div className="!mt-10">
							<button type="submit"
											className="w-full py-3 px-4 text-sm font-semibold rounded text-white bg-blue-500 hover:bg-blue-600 focus:outline-none">
								Create an account
							</button>
						</div>
						<p className="text-sm mt-6 text-center">Already have an account?
							<Button className="text-blue-600 font-semibold hover:underline ml-1"
											onClick={() => signIn(undefined, {callbackUrl: "/dashboard/profile"})}>
								Login here
							</Button>
						</p>
					</form>


				</div>
			</div>

		</>
	)
}