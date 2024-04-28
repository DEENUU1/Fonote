import React from "react";


export default function HeaderText({text}: {text: string}){

	return (
		<>
			<div className="my-6 mx-auto max-w-xl">
				<h1 className="text-3xl font-extrabold text-center">{text}</h1>
			</div>
		</>
	)
}