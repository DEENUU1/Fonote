'use client'

import {useState} from "react";
import Layout from "@/components/Layout";
import React from "react";
import {Input} from "@nextui-org/react";
import {Textarea} from "@nextui-org/react";
import {Button} from "@nextui-org/react";

export default function Contact() {
  const [isLoading, setIsLoading] = useState<boolean>(false);

	return (
		<>
			<Layout>
				<main>
					{
						<>
							<div className="my-6 mx-auto max-w-xl font-[sans-serif]">
								<h1 className="text-3xl font-extrabold text-center">Contact</h1>
								<form className="mt-8 space-y-4">
									<Input disabled={isLoading} isRequired={true} variant={"faded"} type='text' label={"Name"} placeholder='John Doe'/>
									<Input disabled={isLoading} isRequired={true} variant={"faded"} type='email' label={"Email"} placeholder='Email'/>
									<Input disabled={isLoading} isRequired={true} variant={"faded"} type='text' label={"Subject"} placeholder='Subject'/>
									<Textarea disabled={isLoading}  isRequired={true} variant={"faded"} label={"Message"} placeholder='Message'></Textarea>
									<Button isLoading={isLoading} type='button'
													className="text-white bg-blue-500 hover:bg-blue-600 font-semibold rounded-md text-sm px-4 py-3 w-full">{isLoading ? 'Sending...' : 'Send'}
									</Button>
								</form>
							</div>
						</>
					}
				</main>
			</Layout>
		</>
	);
}