import {Chip} from "@nextui-org/react";


export default function ChipStatus({status}: { status: string }) {

	if (status === "NEW") {
		return (
			<>
				<Chip color={"default"} size={"sm"} variant={"flat"}>{status}</Chip>
			</>
		)
	}

	if (status === "PROCESSING") {
		return (
		<>
			<Chip color={"primary"} size={"sm"} variant={"flat"}>{status}</Chip>
		</>
		)
	}

	if (status === "DONE") {
		return (
		<>
			<Chip color={"success"} size={"sm"} variant={"flat"}>{status}</Chip>
		</>
		)
	}

	if (status === "ERROR") {
		return (
		<>
			<Chip color={"warning"} size={"sm"} variant={"flat"}>{status}</Chip>
		</>
		)
	}


}