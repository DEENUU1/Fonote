import Link from "next/link";
import React from "react";


export default function ProfileNavigationLinks() {


	return (
		<>
			<div className={"flex items-center justify-center gap-2"}>
				<Link
					className="rounded-full w-full max-w-[150px] py-4 text-center justify-center items-center bg-blue-600 font-semibold text-lg text-white flex transition-all duration-500 hover:bg-blue-700"
					href={"/dashboard/profile/order"}
				>
					Order history
				</Link>
				<Link
					className="rounded-full w-full max-w-[150px] py-4 text-center justify-center items-center bg-blue-600 font-semibold text-lg text-white flex transition-all duration-500 hover:bg-blue-700"
					href={"/dashboard/profile/subscription"}
				>
					Subscription
				</Link>
			</div>
		</>
	)
}