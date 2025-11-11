--
-- PostgreSQL database dump
--

\restrict jNkE1rdtGBoMYdHpe4XjxLyvPEQCBqKZ8GhAuMgGM7vwjGmTZn0IjcdsK094MY2

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg130+1)
-- Dumped by pg_dump version 17.6

-- Started on 2025-11-11 10:01:15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 17528)
-- Name: a2rp; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA a2rp;


ALTER SCHEMA a2rp OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 17529)
-- Name: assignment; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.assignment (
    assignment_id integer NOT NULL,
    unique_id character varying(1000),
    task_id integer NOT NULL,
    resource_id integer NOT NULL,
    owner_id integer,
    cost numeric,
    actual_cost numeric,
    work numeric,
    actual_work numeric,
    material_work numeric,
    material_actual_work numeric,
    percent_work_completed integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    actual_start_date timestamp without time zone,
    actual_end_date timestamp without time zone,
    delay numeric,
    start_variance numeric,
    end_variance numeric,
    acwp numeric,
    bcwp numeric,
    bcws numeric,
    type integer,
    resource_type_id integer,
    cost_variance numeric,
    work_variance numeric,
    cv numeric,
    sv numeric,
    vac numeric,
    is_over_allocated boolean,
    peak_units numeric,
    created_revision_counter integer,
    modified_revision_counter integer,
    created_date timestamp without time zone,
    modified_date timestamp without time zone,
    regular_cost numeric,
    remaining_cost numeric,
    actual_regular_cost numeric,
    remaining_regular_cost numeric,
    regular_work numeric,
    remaining_work numeric,
    actual_regular_work numeric,
    remaining_regular_work numeric,
    imputation_ce_a_id integer,
    verify_work_breakdown_structure_id integer,
    element_work_breakdown_structure_id integer,
    organizational_unit_manager_id integer,
    manager_id integer,
    executor_cost_center_id integer,
    activity_with_processing_order boolean,
    internal_work boolean,
    wp_status_id integer
);


ALTER TABLE a2rp.assignment OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17534)
-- Name: assignment_assignment_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.assignment_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.assignment_assignment_id_seq OWNER TO postgres;

--
-- TOC entry 3732 (class 0 OID 0)
-- Dependencies: 219
-- Name: assignment_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.assignment_assignment_id_seq OWNED BY a2rp.assignment.assignment_id;


--
-- TOC entry 220 (class 1259 OID 17535)
-- Name: assignment_by_month; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.assignment_by_month (
    assignment_by_month_id integer NOT NULL,
    month date,
    assignment_id integer NOT NULL,
    project_id integer NOT NULL,
    task_id integer NOT NULL,
    cost numeric,
    overtime_cost numeric,
    actual_cost numeric,
    actual_overtime_cost numeric,
    work numeric,
    overtime_work numeric,
    actual_work numeric,
    actual_overtime_work numeric,
    material_work numeric,
    material_actual_work numeric,
    budget_cost numeric,
    budget_work numeric,
    budget_material_work numeric,
    resource_plan_work numeric,
    regular_cost numeric,
    remaining_cost numeric,
    remaining_overtime_cost numeric,
    actual_regular_cost numeric,
    remaining_regular_cost numeric,
    regular_work numeric,
    remaining_work numeric,
    remaining_overtime_work numeric,
    actual_regular_work numeric,
    remaining_regular_work numeric
);


ALTER TABLE a2rp.assignment_by_month OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17540)
-- Name: assignment_by_month_assignment_by_month_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.assignment_by_month_assignment_by_month_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.assignment_by_month_assignment_by_month_id_seq OWNER TO postgres;

--
-- TOC entry 3733 (class 0 OID 0)
-- Dependencies: 221
-- Name: assignment_by_month_assignment_by_month_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.assignment_by_month_assignment_by_month_id_seq OWNED BY a2rp.assignment_by_month.assignment_by_month_id;


--
-- TOC entry 222 (class 1259 OID 17541)
-- Name: cost_center; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.cost_center (
    cost_center_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.cost_center OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17546)
-- Name: cost_center_cost_center_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.cost_center_cost_center_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.cost_center_cost_center_id_seq OWNER TO postgres;

--
-- TOC entry 3734 (class 0 OID 0)
-- Dependencies: 223
-- Name: cost_center_cost_center_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.cost_center_cost_center_id_seq OWNED BY a2rp.cost_center.cost_center_id;


--
-- TOC entry 224 (class 1259 OID 17547)
-- Name: cost_item; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.cost_item (
    cost_item_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.cost_item OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17552)
-- Name: cost_item_cost_item_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.cost_item_cost_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.cost_item_cost_item_id_seq OWNER TO postgres;

--
-- TOC entry 3735 (class 0 OID 0)
-- Dependencies: 225
-- Name: cost_item_cost_item_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.cost_item_cost_item_id_seq OWNED BY a2rp.cost_item.cost_item_id;


--
-- TOC entry 226 (class 1259 OID 17553)
-- Name: cost_type; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.cost_type (
    cost_type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.cost_type OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17558)
-- Name: cost_type_cost_type_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.cost_type_cost_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.cost_type_cost_type_id_seq OWNER TO postgres;

--
-- TOC entry 3736 (class 0 OID 0)
-- Dependencies: 227
-- Name: cost_type_cost_type_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.cost_type_cost_type_id_seq OWNED BY a2rp.cost_type.cost_type_id;


--
-- TOC entry 228 (class 1259 OID 17559)
-- Name: customer; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.customer (
    customer_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    alias text
);


ALTER TABLE a2rp.customer OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17564)
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.customer_customer_id_seq OWNER TO postgres;

--
-- TOC entry 3737 (class 0 OID 0)
-- Dependencies: 229
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.customer_customer_id_seq OWNED BY a2rp.customer.customer_id;


--
-- TOC entry 230 (class 1259 OID 17565)
-- Name: historical_project_summary; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.historical_project_summary (
    historical_project_summary_id integer NOT NULL,
    month date,
    object character varying(255) NOT NULL,
    object_type character varying(20) NOT NULL,
    cost numeric
);


ALTER TABLE a2rp.historical_project_summary OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17570)
-- Name: historical_project_summary_historical_project_summary_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.historical_project_summary_historical_project_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.historical_project_summary_historical_project_summary_id_seq OWNER TO postgres;

--
-- TOC entry 3738 (class 0 OID 0)
-- Dependencies: 231
-- Name: historical_project_summary_historical_project_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.historical_project_summary_historical_project_summary_id_seq OWNED BY a2rp.historical_project_summary.historical_project_summary_id;


--
-- TOC entry 232 (class 1259 OID 17571)
-- Name: historical_project_summary_resource; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.historical_project_summary_resource (
    historical_project_summary_id integer NOT NULL,
    resource_id integer NOT NULL,
    cost_item_id integer NOT NULL,
    cost numeric
);


ALTER TABLE a2rp.historical_project_summary_resource OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17576)
-- Name: imputation; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.imputation (
    imputation_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    alias text
);


ALTER TABLE a2rp.imputation OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17581)
-- Name: imputation_imputation_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.imputation_imputation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.imputation_imputation_id_seq OWNER TO postgres;

--
-- TOC entry 3739 (class 0 OID 0)
-- Dependencies: 234
-- Name: imputation_imputation_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.imputation_imputation_id_seq OWNED BY a2rp.imputation.imputation_id;


--
-- TOC entry 235 (class 1259 OID 17582)
-- Name: job; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.job (
    job_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    alias text
);


ALTER TABLE a2rp.job OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17587)
-- Name: job_job_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.job_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.job_job_id_seq OWNER TO postgres;

--
-- TOC entry 3740 (class 0 OID 0)
-- Dependencies: 236
-- Name: job_job_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.job_job_id_seq OWNED BY a2rp.job.job_id;


--
-- TOC entry 237 (class 1259 OID 17588)
-- Name: nt_account; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.nt_account (
    nt_account_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    alias text
);


ALTER TABLE a2rp.nt_account OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17593)
-- Name: nt_account_nt_account_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.nt_account_nt_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.nt_account_nt_account_id_seq OWNER TO postgres;

--
-- TOC entry 3741 (class 0 OID 0)
-- Dependencies: 238
-- Name: nt_account_nt_account_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.nt_account_nt_account_id_seq OWNED BY a2rp.nt_account.nt_account_id;


--
-- TOC entry 239 (class 1259 OID 17594)
-- Name: organizational_unit; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.organizational_unit (
    organizational_unit_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    alias text,
    rate numeric,
    monthly_hours_availability numeric
);


ALTER TABLE a2rp.organizational_unit OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17599)
-- Name: organizational_unit_organizational_unit_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.organizational_unit_organizational_unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.organizational_unit_organizational_unit_id_seq OWNER TO postgres;

--
-- TOC entry 3742 (class 0 OID 0)
-- Dependencies: 240
-- Name: organizational_unit_organizational_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.organizational_unit_organizational_unit_id_seq OWNED BY a2rp.organizational_unit.organizational_unit_id;


--
-- TOC entry 241 (class 1259 OID 17600)
-- Name: processing_order; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.processing_order (
    processing_order_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    project_code character varying(100),
    project_id integer,
    task_id integer,
    phase integer,
    processing_order_type_id integer,
    processing_order_status_id integer,
    work_breakdown_structure_id integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    release_date timestamp without time zone,
    modified_date timestamp without time zone,
    program_manager_id integer,
    project_manager_id integer,
    row_state_processing_order_shark character varying(100),
    technical_feature_id integer,
    value_id integer
);


ALTER TABLE a2rp.processing_order OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17605)
-- Name: processing_order_processing_order_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.processing_order_processing_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.processing_order_processing_order_id_seq OWNER TO postgres;

--
-- TOC entry 3743 (class 0 OID 0)
-- Dependencies: 242
-- Name: processing_order_processing_order_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.processing_order_processing_order_id_seq OWNED BY a2rp.processing_order.processing_order_id;


--
-- TOC entry 243 (class 1259 OID 17606)
-- Name: processing_order_status; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.processing_order_status (
    processing_order_status_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.processing_order_status OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17611)
-- Name: processing_order_status_processing_order_status_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.processing_order_status_processing_order_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.processing_order_status_processing_order_status_id_seq OWNER TO postgres;

--
-- TOC entry 3744 (class 0 OID 0)
-- Dependencies: 244
-- Name: processing_order_status_processing_order_status_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.processing_order_status_processing_order_status_id_seq OWNED BY a2rp.processing_order_status.processing_order_status_id;


--
-- TOC entry 245 (class 1259 OID 17612)
-- Name: processing_order_type; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.processing_order_type (
    processing_order_type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.processing_order_type OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17617)
-- Name: processing_order_type_processing_order_type_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.processing_order_type_processing_order_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.processing_order_type_processing_order_type_id_seq OWNER TO postgres;

--
-- TOC entry 3745 (class 0 OID 0)
-- Dependencies: 246
-- Name: processing_order_type_processing_order_type_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.processing_order_type_processing_order_type_id_seq OWNED BY a2rp.processing_order_type.processing_order_type_id;


--
-- TOC entry 247 (class 1259 OID 17618)
-- Name: project; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.project (
    project_id integer NOT NULL,
    unique_id character varying(1000),
    name character varying(255) NOT NULL,
    description text,
    author_id integer,
    owner_id integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    status_date timestamp without time zone,
    project_type_id integer NOT NULL,
    workspace_internal_h_ref character varying(100),
    calculations_are_stale boolean,
    modified_revision_counter integer,
    created_date timestamp without time zone,
    modified_date timestamp without time zone,
    calendar_duration numeric,
    parent_id integer,
    cost numeric,
    actual_cost numeric,
    work numeric,
    actual_work numeric,
    duration_variance numeric,
    start_variance numeric,
    end_variance numeric,
    duration numeric,
    actual_duration numeric,
    actual_start_date timestamp without time zone,
    actual_end_date timestamp without time zone,
    percent_completed integer,
    percent_work_completed integer,
    acwp numeric,
    bcws numeric,
    spi numeric,
    tcpi numeric,
    vac numeric,
    eac numeric,
    cost_variance numeric,
    cv numeric,
    cpi numeric,
    early_start timestamp without time zone,
    early_end timestamp without time zone,
    late_start timestamp without time zone,
    late_end timestamp without time zone,
    sv numeric,
    work_variance numeric,
    regular_cost numeric,
    remaining_cost numeric,
    actual_regular_cost numeric,
    remaining_regular_cost numeric,
    regular_work numeric,
    remaining_work numeric,
    actual_regular_work numeric,
    remaining_regular_work numeric,
    cvp numeric,
    svp numeric,
    baseline0_cost numeric,
    baseline0_work numeric,
    baseline0_start_date timestamp without time zone,
    baseline0_end_date timestamp without time zone,
    baseline0_duration numeric,
    baseline1_cost numeric,
    baseline1_work numeric,
    baseline1_start_date timestamp without time zone,
    baseline1_end_date timestamp without time zone,
    baseline1_duration numeric,
    baseline6_cost numeric,
    baseline6_work numeric,
    baseline6_start_date timestamp without time zone,
    baseline6_end_date timestamp without time zone,
    baseline6_duration numeric,
    baseline10_fixed_cost numeric,
    budget_current_year numeric,
    budget numeric,
    total_cost numeric,
    program_manager_id integer,
    imputation_id integer,
    project_manager_id integer,
    project_status_id integer NOT NULL,
    fes_offer boolean,
    accounting_sector character varying(100),
    contract_start_date timestamp without time zone,
    prev_cost numeric,
    finalized_cost numeric,
    residual_cost numeric,
    work_breakdown_structure_id integer,
    customer_id integer,
    project_manager_organizational_unit_id integer,
    alias text
);


ALTER TABLE a2rp.project OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17623)
-- Name: project_project_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.project_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.project_project_id_seq OWNER TO postgres;

--
-- TOC entry 3746 (class 0 OID 0)
-- Dependencies: 248
-- Name: project_project_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.project_project_id_seq OWNED BY a2rp.project.project_id;


--
-- TOC entry 249 (class 1259 OID 17624)
-- Name: project_status; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.project_status (
    project_status_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.project_status OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 17629)
-- Name: project_status_project_status_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.project_status_project_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.project_status_project_status_id_seq OWNER TO postgres;

--
-- TOC entry 3747 (class 0 OID 0)
-- Dependencies: 250
-- Name: project_status_project_status_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.project_status_project_status_id_seq OWNED BY a2rp.project_status.project_status_id;


--
-- TOC entry 251 (class 1259 OID 17630)
-- Name: project_to_plan; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.project_to_plan (
    project_to_plan_id integer NOT NULL,
    description text,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    imputation_id integer,
    responsible integer,
    total numeric,
    labour_cost numeric,
    third_party_supplies numeric,
    expences numeric,
    consultants numeric,
    materials numeric,
    labour_cost_2 numeric,
    project_costs numeric,
    notes text,
    prob numeric,
    impact numeric,
    risk_value numeric,
    risk numeric,
    risk_description character varying(100),
    prob_2 numeric,
    saving numeric,
    opportunity_value numeric,
    value numeric,
    opportunity_description character varying(100)
);


ALTER TABLE a2rp.project_to_plan OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 17635)
-- Name: project_to_plan_organizational_unit; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.project_to_plan_organizational_unit (
    project_to_plan_id integer NOT NULL,
    organizational_unit_id integer NOT NULL,
    hours numeric
);


ALTER TABLE a2rp.project_to_plan_organizational_unit OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 17640)
-- Name: project_to_plan_project_to_plan_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.project_to_plan_project_to_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.project_to_plan_project_to_plan_id_seq OWNER TO postgres;

--
-- TOC entry 3748 (class 0 OID 0)
-- Dependencies: 253
-- Name: project_to_plan_project_to_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.project_to_plan_project_to_plan_id_seq OWNED BY a2rp.project_to_plan.project_to_plan_id;


--
-- TOC entry 254 (class 1259 OID 17641)
-- Name: project_type; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.project_type (
    project_type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.project_type OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 17646)
-- Name: project_type_project_type_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.project_type_project_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.project_type_project_type_id_seq OWNER TO postgres;

--
-- TOC entry 3749 (class 0 OID 0)
-- Dependencies: 255
-- Name: project_type_project_type_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.project_type_project_type_id_seq OWNED BY a2rp.project_type.project_type_id;


--
-- TOC entry 256 (class 1259 OID 17647)
-- Name: property; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.property (
    property_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.property OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 17652)
-- Name: property_property_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.property_property_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.property_property_id_seq OWNER TO postgres;

--
-- TOC entry 3750 (class 0 OID 0)
-- Dependencies: 257
-- Name: property_property_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.property_property_id_seq OWNED BY a2rp.property.property_id;


--
-- TOC entry 258 (class 1259 OID 17653)
-- Name: resource; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.resource (
    resource_id integer NOT NULL,
    unique_id character varying(1000),
    name character varying(255) NOT NULL,
    standard_rate numeric,
    resource_status_id integer NOT NULL,
    resource_type_id integer NOT NULL,
    code character varying(100),
    mail_address character varying(100),
    initials character varying(10),
    max_units integer,
    booking_type integer,
    timesheet_manager_id integer,
    earliest_available_from timestamp without time zone,
    latest_available_to timestamp without time zone,
    can_level boolean,
    nt_account_id integer,
    is_active boolean,
    is_generic boolean,
    is_team boolean,
    base_calendar character varying(100),
    client_unique_id integer,
    resource_cost_center_id integer,
    modified_revision_counter integer,
    created_date timestamp without time zone,
    modified_date timestamp without time zone,
    organizational_unit_id integer,
    resource_breakdown_structure_2_id integer,
    resource_organizational_unit_id integer,
    resource_breakdown_structure_1_id integer,
    property_id integer,
    resource_breakdown_structure_id integer,
    internal_work boolean,
    cost_center_id integer,
    tda character varying(100),
    job_id integer,
    alias text
);


ALTER TABLE a2rp.resource OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 17658)
-- Name: resource_breakdown_structure; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.resource_breakdown_structure (
    resource_breakdown_structure_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.resource_breakdown_structure OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 17663)
-- Name: resource_breakdown_structure_resource_breakdown_structure_i_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.resource_breakdown_structure_resource_breakdown_structure_i_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.resource_breakdown_structure_resource_breakdown_structure_i_seq OWNER TO postgres;

--
-- TOC entry 3751 (class 0 OID 0)
-- Dependencies: 260
-- Name: resource_breakdown_structure_resource_breakdown_structure_i_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.resource_breakdown_structure_resource_breakdown_structure_i_seq OWNED BY a2rp.resource_breakdown_structure.resource_breakdown_structure_id;


--
-- TOC entry 261 (class 1259 OID 17664)
-- Name: resource_resource_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.resource_resource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.resource_resource_id_seq OWNER TO postgres;

--
-- TOC entry 3752 (class 0 OID 0)
-- Dependencies: 261
-- Name: resource_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.resource_resource_id_seq OWNED BY a2rp.resource.resource_id;


--
-- TOC entry 262 (class 1259 OID 17665)
-- Name: resource_status; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.resource_status (
    resource_status_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.resource_status OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 17670)
-- Name: resource_status_resource_status_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.resource_status_resource_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.resource_status_resource_status_id_seq OWNER TO postgres;

--
-- TOC entry 3753 (class 0 OID 0)
-- Dependencies: 263
-- Name: resource_status_resource_status_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.resource_status_resource_status_id_seq OWNED BY a2rp.resource_status.resource_status_id;


--
-- TOC entry 264 (class 1259 OID 17671)
-- Name: resource_type; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.resource_type (
    resource_type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.resource_type OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 17676)
-- Name: resource_type_resource_type_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.resource_type_resource_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.resource_type_resource_type_id_seq OWNER TO postgres;

--
-- TOC entry 3754 (class 0 OID 0)
-- Dependencies: 265
-- Name: resource_type_resource_type_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.resource_type_resource_type_id_seq OWNED BY a2rp.resource_type.resource_type_id;


--
-- TOC entry 266 (class 1259 OID 17677)
-- Name: task; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.task (
    task_id integer NOT NULL,
    unique_id character varying(1000),
    name character varying(255) NOT NULL,
    description text,
    parent_id integer,
    task_status_id integer NOT NULL,
    project_id integer,
    fixed_cost_assignment_uid character varying(100),
    task_priority integer,
    task_index integer,
    is_overallocated boolean,
    is_project_summary boolean,
    outline_level integer,
    outline_number character varying(100),
    is_milestone boolean,
    is_critical boolean,
    is_summary boolean,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    fixed_cost numeric,
    actual_fixed_cost numeric,
    cost numeric,
    actual_cost numeric,
    actual_overtime_cost numeric,
    work numeric,
    overtime_work numeric,
    actual_work numeric,
    actual_overtime_work numeric,
    duration_variance numeric,
    start_variance numeric,
    end_variance numeric,
    actual_start_date timestamp without time zone,
    actual_end_date timestamp without time zone,
    duration numeric,
    actual_duration numeric,
    deliverable_start_date timestamp without time zone,
    deliverable_end_date timestamp without time zone,
    percent_completed integer,
    percent_work_completed integer,
    physical_percent_completed integer,
    acwp integer,
    bcwp integer,
    bcws integer,
    spi integer,
    tcpi integer,
    vac integer,
    deadline timestamp without time zone,
    duration_is_estimated boolean,
    is_effort_driven boolean,
    is_external boolean,
    is_recurring boolean,
    total_slack numeric,
    free_slack numeric,
    eac integer,
    cost_variance numeric,
    cv numeric,
    cpi numeric,
    early_start timestamp without time zone,
    early_end timestamp without time zone,
    late_start timestamp without time zone,
    late_end timestamp without time zone,
    sv numeric,
    work_variance numeric,
    ignores_resource_calendar boolean,
    client_unique_id integer,
    is_marked boolean,
    wbs_tree character varying(100),
    created_revision_counter integer,
    modified_revision_counter integer,
    created_date timestamp without time zone,
    modified_date timestamp without time zone,
    cvp numeric,
    svp numeric,
    regular_cost numeric,
    remaining_cost numeric,
    remaining_overtime_cost numeric,
    actual_regular_cost numeric,
    remaining_regular_cost numeric,
    regular_work numeric,
    remaining_work numeric,
    remaining_overtime_work numeric,
    actual_regular_work numeric,
    remaining_regular_work numeric,
    remaining_duration numeric,
    processing_order_id integer,
    imputation_ce_id integer,
    imputation_ce_old_id integer,
    milestone_estimated_end_date timestamp without time zone,
    contractual_milestone character varying(100),
    verify_work_breakdown_structure_id integer,
    element_work_breakdown_structure_id integer,
    organizational_unit_manager_id integer,
    manager_id integer,
    executor_cost_center_id integer,
    cost_center_id integer,
    activity_with_processing_order boolean,
    engagement numeric,
    available_cost numeric,
    validity_date timestamp without time zone,
    project_status_id integer,
    milestone_project character varying(100),
    activity_group character varying(100),
    wp_status_id integer,
    output_task character varying(100),
    phase character varying(100),
    alias text,
    processing_order_actual_cost numeric
);


ALTER TABLE a2rp.task OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 17682)
-- Name: task_status; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.task_status (
    task_status_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.task_status OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 17687)
-- Name: task_status_task_status_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.task_status_task_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.task_status_task_status_id_seq OWNER TO postgres;

--
-- TOC entry 3755 (class 0 OID 0)
-- Dependencies: 268
-- Name: task_status_task_status_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.task_status_task_status_id_seq OWNED BY a2rp.task_status.task_status_id;


--
-- TOC entry 269 (class 1259 OID 17688)
-- Name: task_task_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.task_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.task_task_id_seq OWNER TO postgres;

--
-- TOC entry 3756 (class 0 OID 0)
-- Dependencies: 269
-- Name: task_task_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.task_task_id_seq OWNED BY a2rp.task.task_id;


--
-- TOC entry 270 (class 1259 OID 17689)
-- Name: task_to_plan; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.task_to_plan (
    task_to_plan_id integer NOT NULL,
    wp_id character varying(100),
    description text,
    row_type character varying(15),
    is_milestone boolean,
    previous text,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    project_to_plan_id integer,
    responsible integer,
    total numeric,
    labour_cost numeric,
    third_party_supplies numeric,
    expences numeric,
    consultants numeric,
    materials numeric,
    labour_cost_2 numeric,
    project_costs numeric,
    notes text,
    prob numeric,
    impact numeric,
    risk_value numeric,
    risk numeric,
    risk_description character varying(100),
    prob_2 numeric,
    saving numeric,
    opportunity_value numeric,
    value numeric,
    opportunity_description character varying(100)
);


ALTER TABLE a2rp.task_to_plan OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 17694)
-- Name: task_to_plan_organizational_unit; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.task_to_plan_organizational_unit (
    task_to_plan_id integer NOT NULL,
    organizational_unit_id integer NOT NULL,
    hours numeric,
    project_to_plan_id integer
);


ALTER TABLE a2rp.task_to_plan_organizational_unit OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 17699)
-- Name: task_to_plan_task_to_plan_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.task_to_plan_task_to_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.task_to_plan_task_to_plan_id_seq OWNER TO postgres;

--
-- TOC entry 3757 (class 0 OID 0)
-- Dependencies: 272
-- Name: task_to_plan_task_to_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.task_to_plan_task_to_plan_id_seq OWNED BY a2rp.task_to_plan.task_to_plan_id;


--
-- TOC entry 273 (class 1259 OID 17700)
-- Name: technical_feature; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.technical_feature (
    technical_feature_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE a2rp.technical_feature OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 17705)
-- Name: technical_feature_technical_feature_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.technical_feature_technical_feature_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.technical_feature_technical_feature_id_seq OWNER TO postgres;

--
-- TOC entry 3758 (class 0 OID 0)
-- Dependencies: 274
-- Name: technical_feature_technical_feature_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.technical_feature_technical_feature_id_seq OWNED BY a2rp.technical_feature.technical_feature_id;


--
-- TOC entry 275 (class 1259 OID 17706)
-- Name: work_breakdown_structure; Type: TABLE; Schema: a2rp; Owner: postgres
--

CREATE TABLE a2rp.work_breakdown_structure (
    work_breakdown_structure_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    project_id integer
);


ALTER TABLE a2rp.work_breakdown_structure OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 17711)
-- Name: work_breakdown_structure_work_breakdown_structure_id_seq; Type: SEQUENCE; Schema: a2rp; Owner: postgres
--

CREATE SEQUENCE a2rp.work_breakdown_structure_work_breakdown_structure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE a2rp.work_breakdown_structure_work_breakdown_structure_id_seq OWNER TO postgres;

--
-- TOC entry 3759 (class 0 OID 0)
-- Dependencies: 276
-- Name: work_breakdown_structure_work_breakdown_structure_id_seq; Type: SEQUENCE OWNED BY; Schema: a2rp; Owner: postgres
--

ALTER SEQUENCE a2rp.work_breakdown_structure_work_breakdown_structure_id_seq OWNED BY a2rp.work_breakdown_structure.work_breakdown_structure_id;


--
-- TOC entry 278 (class 1259 OID 18139)
-- Name: ckrgky205xwebcuq_chat_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ckrgky205xwebcuq_chat_history (
    id integer NOT NULL,
    session_id character varying(255) NOT NULL,
    message jsonb NOT NULL
);


ALTER TABLE public.ckrgky205xwebcuq_chat_history OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 18138)
-- Name: ckrgky205xwebcuq_chat_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ckrgky205xwebcuq_chat_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ckrgky205xwebcuq_chat_history_id_seq OWNER TO postgres;

--
-- TOC entry 3760 (class 0 OID 0)
-- Dependencies: 277
-- Name: ckrgky205xwebcuq_chat_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ckrgky205xwebcuq_chat_history_id_seq OWNED BY public.ckrgky205xwebcuq_chat_history.id;


--
-- TOC entry 3427 (class 2604 OID 17712)
-- Name: assignment assignment_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment ALTER COLUMN assignment_id SET DEFAULT nextval('a2rp.assignment_assignment_id_seq'::regclass);


--
-- TOC entry 3428 (class 2604 OID 17713)
-- Name: assignment_by_month assignment_by_month_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment_by_month ALTER COLUMN assignment_by_month_id SET DEFAULT nextval('a2rp.assignment_by_month_assignment_by_month_id_seq'::regclass);


--
-- TOC entry 3429 (class 2604 OID 17714)
-- Name: cost_center cost_center_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_center ALTER COLUMN cost_center_id SET DEFAULT nextval('a2rp.cost_center_cost_center_id_seq'::regclass);


--
-- TOC entry 3430 (class 2604 OID 17715)
-- Name: cost_item cost_item_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_item ALTER COLUMN cost_item_id SET DEFAULT nextval('a2rp.cost_item_cost_item_id_seq'::regclass);


--
-- TOC entry 3431 (class 2604 OID 17716)
-- Name: cost_type cost_type_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_type ALTER COLUMN cost_type_id SET DEFAULT nextval('a2rp.cost_type_cost_type_id_seq'::regclass);


--
-- TOC entry 3432 (class 2604 OID 17717)
-- Name: customer customer_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.customer ALTER COLUMN customer_id SET DEFAULT nextval('a2rp.customer_customer_id_seq'::regclass);


--
-- TOC entry 3433 (class 2604 OID 17718)
-- Name: historical_project_summary historical_project_summary_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary ALTER COLUMN historical_project_summary_id SET DEFAULT nextval('a2rp.historical_project_summary_historical_project_summary_id_seq'::regclass);


--
-- TOC entry 3434 (class 2604 OID 17719)
-- Name: imputation imputation_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.imputation ALTER COLUMN imputation_id SET DEFAULT nextval('a2rp.imputation_imputation_id_seq'::regclass);


--
-- TOC entry 3435 (class 2604 OID 17720)
-- Name: job job_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.job ALTER COLUMN job_id SET DEFAULT nextval('a2rp.job_job_id_seq'::regclass);


--
-- TOC entry 3436 (class 2604 OID 17721)
-- Name: nt_account nt_account_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.nt_account ALTER COLUMN nt_account_id SET DEFAULT nextval('a2rp.nt_account_nt_account_id_seq'::regclass);


--
-- TOC entry 3437 (class 2604 OID 17722)
-- Name: organizational_unit organizational_unit_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.organizational_unit ALTER COLUMN organizational_unit_id SET DEFAULT nextval('a2rp.organizational_unit_organizational_unit_id_seq'::regclass);


--
-- TOC entry 3438 (class 2604 OID 17723)
-- Name: processing_order processing_order_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order ALTER COLUMN processing_order_id SET DEFAULT nextval('a2rp.processing_order_processing_order_id_seq'::regclass);


--
-- TOC entry 3439 (class 2604 OID 17724)
-- Name: processing_order_status processing_order_status_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order_status ALTER COLUMN processing_order_status_id SET DEFAULT nextval('a2rp.processing_order_status_processing_order_status_id_seq'::regclass);


--
-- TOC entry 3440 (class 2604 OID 17725)
-- Name: processing_order_type processing_order_type_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order_type ALTER COLUMN processing_order_type_id SET DEFAULT nextval('a2rp.processing_order_type_processing_order_type_id_seq'::regclass);


--
-- TOC entry 3441 (class 2604 OID 17726)
-- Name: project project_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project ALTER COLUMN project_id SET DEFAULT nextval('a2rp.project_project_id_seq'::regclass);


--
-- TOC entry 3442 (class 2604 OID 17727)
-- Name: project_status project_status_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_status ALTER COLUMN project_status_id SET DEFAULT nextval('a2rp.project_status_project_status_id_seq'::regclass);


--
-- TOC entry 3443 (class 2604 OID 17728)
-- Name: project_to_plan project_to_plan_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_to_plan ALTER COLUMN project_to_plan_id SET DEFAULT nextval('a2rp.project_to_plan_project_to_plan_id_seq'::regclass);


--
-- TOC entry 3444 (class 2604 OID 17729)
-- Name: project_type project_type_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_type ALTER COLUMN project_type_id SET DEFAULT nextval('a2rp.project_type_project_type_id_seq'::regclass);


--
-- TOC entry 3445 (class 2604 OID 17730)
-- Name: property property_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.property ALTER COLUMN property_id SET DEFAULT nextval('a2rp.property_property_id_seq'::regclass);


--
-- TOC entry 3446 (class 2604 OID 17731)
-- Name: resource resource_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource ALTER COLUMN resource_id SET DEFAULT nextval('a2rp.resource_resource_id_seq'::regclass);


--
-- TOC entry 3447 (class 2604 OID 17732)
-- Name: resource_breakdown_structure resource_breakdown_structure_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_breakdown_structure ALTER COLUMN resource_breakdown_structure_id SET DEFAULT nextval('a2rp.resource_breakdown_structure_resource_breakdown_structure_i_seq'::regclass);


--
-- TOC entry 3448 (class 2604 OID 17733)
-- Name: resource_status resource_status_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_status ALTER COLUMN resource_status_id SET DEFAULT nextval('a2rp.resource_status_resource_status_id_seq'::regclass);


--
-- TOC entry 3449 (class 2604 OID 17734)
-- Name: resource_type resource_type_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_type ALTER COLUMN resource_type_id SET DEFAULT nextval('a2rp.resource_type_resource_type_id_seq'::regclass);


--
-- TOC entry 3450 (class 2604 OID 17735)
-- Name: task task_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task ALTER COLUMN task_id SET DEFAULT nextval('a2rp.task_task_id_seq'::regclass);


--
-- TOC entry 3451 (class 2604 OID 17736)
-- Name: task_status task_status_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task_status ALTER COLUMN task_status_id SET DEFAULT nextval('a2rp.task_status_task_status_id_seq'::regclass);


--
-- TOC entry 3452 (class 2604 OID 17737)
-- Name: task_to_plan task_to_plan_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task_to_plan ALTER COLUMN task_to_plan_id SET DEFAULT nextval('a2rp.task_to_plan_task_to_plan_id_seq'::regclass);


--
-- TOC entry 3453 (class 2604 OID 17738)
-- Name: technical_feature technical_feature_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.technical_feature ALTER COLUMN technical_feature_id SET DEFAULT nextval('a2rp.technical_feature_technical_feature_id_seq'::regclass);


--
-- TOC entry 3454 (class 2604 OID 17739)
-- Name: work_breakdown_structure work_breakdown_structure_id; Type: DEFAULT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.work_breakdown_structure ALTER COLUMN work_breakdown_structure_id SET DEFAULT nextval('a2rp.work_breakdown_structure_work_breakdown_structure_id_seq'::regclass);


--
-- TOC entry 3455 (class 2604 OID 18142)
-- Name: ckrgky205xwebcuq_chat_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ckrgky205xwebcuq_chat_history ALTER COLUMN id SET DEFAULT nextval('public.ckrgky205xwebcuq_chat_history_id_seq'::regclass);


--
-- TOC entry 3459 (class 2606 OID 17767)
-- Name: assignment_by_month assignment_by_month_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment_by_month
    ADD CONSTRAINT assignment_by_month_pk PRIMARY KEY (assignment_by_month_id);


--
-- TOC entry 3457 (class 2606 OID 17769)
-- Name: assignment assignment_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_pk PRIMARY KEY (assignment_id);


--
-- TOC entry 3461 (class 2606 OID 17771)
-- Name: cost_center cost_center_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_center
    ADD CONSTRAINT cost_center_pk PRIMARY KEY (cost_center_id);


--
-- TOC entry 3463 (class 2606 OID 17773)
-- Name: cost_item cost_item_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_item
    ADD CONSTRAINT cost_item_pk PRIMARY KEY (cost_item_id);


--
-- TOC entry 3465 (class 2606 OID 17775)
-- Name: cost_type cost_type_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.cost_type
    ADD CONSTRAINT cost_type_pk PRIMARY KEY (cost_type_id);


--
-- TOC entry 3467 (class 2606 OID 17777)
-- Name: customer customer_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.customer
    ADD CONSTRAINT customer_pk PRIMARY KEY (customer_id);


--
-- TOC entry 3469 (class 2606 OID 17779)
-- Name: historical_project_summary historical_project_summary_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary
    ADD CONSTRAINT historical_project_summary_pk PRIMARY KEY (historical_project_summary_id);


--
-- TOC entry 3471 (class 2606 OID 17781)
-- Name: historical_project_summary_resource historical_project_summary_resource_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary_resource
    ADD CONSTRAINT historical_project_summary_resource_pk PRIMARY KEY (historical_project_summary_id, resource_id, cost_item_id);


--
-- TOC entry 3473 (class 2606 OID 17783)
-- Name: imputation imputation_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.imputation
    ADD CONSTRAINT imputation_pk PRIMARY KEY (imputation_id);


--
-- TOC entry 3475 (class 2606 OID 17785)
-- Name: job job_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.job
    ADD CONSTRAINT job_pk PRIMARY KEY (job_id);


--
-- TOC entry 3477 (class 2606 OID 17787)
-- Name: nt_account nt_account_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.nt_account
    ADD CONSTRAINT nt_account_pk PRIMARY KEY (nt_account_id);


--
-- TOC entry 3479 (class 2606 OID 17789)
-- Name: organizational_unit organizational_unit_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.organizational_unit
    ADD CONSTRAINT organizational_unit_pk PRIMARY KEY (organizational_unit_id);


--
-- TOC entry 3481 (class 2606 OID 17791)
-- Name: processing_order processing_order_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_pk PRIMARY KEY (processing_order_id);


--
-- TOC entry 3483 (class 2606 OID 17793)
-- Name: processing_order_status processing_order_status_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order_status
    ADD CONSTRAINT processing_order_status_pk PRIMARY KEY (processing_order_status_id);


--
-- TOC entry 3485 (class 2606 OID 17795)
-- Name: processing_order_type processing_order_type_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order_type
    ADD CONSTRAINT processing_order_type_pk PRIMARY KEY (processing_order_type_id);


--
-- TOC entry 3487 (class 2606 OID 17797)
-- Name: project project_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_pk PRIMARY KEY (project_id);


--
-- TOC entry 3489 (class 2606 OID 17799)
-- Name: project_status project_status_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_status
    ADD CONSTRAINT project_status_pk PRIMARY KEY (project_status_id);


--
-- TOC entry 3493 (class 2606 OID 17801)
-- Name: project_to_plan_organizational_unit project_to_plan_organizational_unit_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_to_plan_organizational_unit
    ADD CONSTRAINT project_to_plan_organizational_unit_pk PRIMARY KEY (project_to_plan_id, organizational_unit_id);


--
-- TOC entry 3491 (class 2606 OID 17803)
-- Name: project_to_plan project_to_plan_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_to_plan
    ADD CONSTRAINT project_to_plan_pk PRIMARY KEY (project_to_plan_id);


--
-- TOC entry 3495 (class 2606 OID 17805)
-- Name: project_type project_type_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project_type
    ADD CONSTRAINT project_type_pk PRIMARY KEY (project_type_id);


--
-- TOC entry 3497 (class 2606 OID 17807)
-- Name: property property_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.property
    ADD CONSTRAINT property_pk PRIMARY KEY (property_id);


--
-- TOC entry 3501 (class 2606 OID 17809)
-- Name: resource_breakdown_structure resource_breakdown_structure_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_breakdown_structure
    ADD CONSTRAINT resource_breakdown_structure_pk PRIMARY KEY (resource_breakdown_structure_id);


--
-- TOC entry 3499 (class 2606 OID 17811)
-- Name: resource resource_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_pk PRIMARY KEY (resource_id);


--
-- TOC entry 3503 (class 2606 OID 17813)
-- Name: resource_status resource_status_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_status
    ADD CONSTRAINT resource_status_pk PRIMARY KEY (resource_status_id);


--
-- TOC entry 3505 (class 2606 OID 17815)
-- Name: resource_type resource_type_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource_type
    ADD CONSTRAINT resource_type_pk PRIMARY KEY (resource_type_id);


--
-- TOC entry 3507 (class 2606 OID 17817)
-- Name: task task_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_pk PRIMARY KEY (task_id);


--
-- TOC entry 3509 (class 2606 OID 17819)
-- Name: task_status task_status_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task_status
    ADD CONSTRAINT task_status_pk PRIMARY KEY (task_status_id);


--
-- TOC entry 3513 (class 2606 OID 17821)
-- Name: task_to_plan_organizational_unit task_to_plan_organizational_unit_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task_to_plan_organizational_unit
    ADD CONSTRAINT task_to_plan_organizational_unit_pk PRIMARY KEY (task_to_plan_id, organizational_unit_id);


--
-- TOC entry 3511 (class 2606 OID 17823)
-- Name: task_to_plan task_to_plan_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task_to_plan
    ADD CONSTRAINT task_to_plan_pk PRIMARY KEY (task_to_plan_id);


--
-- TOC entry 3515 (class 2606 OID 17825)
-- Name: technical_feature technical_feature_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.technical_feature
    ADD CONSTRAINT technical_feature_pk PRIMARY KEY (technical_feature_id);


--
-- TOC entry 3517 (class 2606 OID 17827)
-- Name: work_breakdown_structure work_breakdown_structure_pk; Type: CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.work_breakdown_structure
    ADD CONSTRAINT work_breakdown_structure_pk PRIMARY KEY (work_breakdown_structure_id);


--
-- TOC entry 3519 (class 2606 OID 18146)
-- Name: ckrgky205xwebcuq_chat_history ckrgky205xwebcuq_chat_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ckrgky205xwebcuq_chat_history
    ADD CONSTRAINT ckrgky205xwebcuq_chat_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3530 (class 2606 OID 17828)
-- Name: assignment_by_month assignment_by_month_assignment_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment_by_month
    ADD CONSTRAINT assignment_by_month_assignment_fk FOREIGN KEY (assignment_id) REFERENCES a2rp.assignment(assignment_id) ON DELETE CASCADE;


--
-- TOC entry 3531 (class 2606 OID 17833)
-- Name: assignment_by_month assignment_by_month_project_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment_by_month
    ADD CONSTRAINT assignment_by_month_project_fk FOREIGN KEY (project_id) REFERENCES a2rp.project(project_id) ON DELETE CASCADE;


--
-- TOC entry 3532 (class 2606 OID 17838)
-- Name: assignment_by_month assignment_by_month_task_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment_by_month
    ADD CONSTRAINT assignment_by_month_task_fk FOREIGN KEY (task_id) REFERENCES a2rp.task(task_id) ON DELETE CASCADE;


--
-- TOC entry 3520 (class 2606 OID 17843)
-- Name: assignment assignment_cost_center_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_cost_center_fk FOREIGN KEY (executor_cost_center_id) REFERENCES a2rp.cost_center(cost_center_id) ON DELETE CASCADE;


--
-- TOC entry 3521 (class 2606 OID 17848)
-- Name: assignment assignment_imputation_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_imputation_fk FOREIGN KEY (imputation_ce_a_id) REFERENCES a2rp.imputation(imputation_id) ON DELETE CASCADE;


--
-- TOC entry 3522 (class 2606 OID 17853)
-- Name: assignment assignment_organizational_unit_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_organizational_unit_fk FOREIGN KEY (organizational_unit_manager_id) REFERENCES a2rp.organizational_unit(organizational_unit_id) ON DELETE CASCADE;


--
-- TOC entry 3523 (class 2606 OID 17858)
-- Name: assignment assignment_resource_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_resource_2_fk FOREIGN KEY (owner_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3524 (class 2606 OID 17863)
-- Name: assignment assignment_resource_3_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_resource_3_fk FOREIGN KEY (manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3525 (class 2606 OID 17868)
-- Name: assignment assignment_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_resource_fk FOREIGN KEY (resource_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3526 (class 2606 OID 17873)
-- Name: assignment assignment_resource_type_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_resource_type_fk FOREIGN KEY (resource_type_id) REFERENCES a2rp.resource_type(resource_type_id) ON DELETE CASCADE;


--
-- TOC entry 3527 (class 2606 OID 17878)
-- Name: assignment assignment_task_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_task_fk FOREIGN KEY (task_id) REFERENCES a2rp.task(task_id) ON DELETE CASCADE;


--
-- TOC entry 3528 (class 2606 OID 17883)
-- Name: assignment assignment_work_breakdown_structure_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_work_breakdown_structure_2_fk FOREIGN KEY (element_work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3529 (class 2606 OID 17888)
-- Name: assignment assignment_work_breakdown_structure_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.assignment
    ADD CONSTRAINT assignment_work_breakdown_structure_fk FOREIGN KEY (verify_work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3533 (class 2606 OID 17893)
-- Name: historical_project_summary_resource historical_project_summary_resource_cost_item_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary_resource
    ADD CONSTRAINT historical_project_summary_resource_cost_item_fk FOREIGN KEY (cost_item_id) REFERENCES a2rp.cost_item(cost_item_id) ON DELETE CASCADE;


--
-- TOC entry 3534 (class 2606 OID 17898)
-- Name: historical_project_summary_resource historical_project_summary_resource_historical_project_summary_; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary_resource
    ADD CONSTRAINT historical_project_summary_resource_historical_project_summary_ FOREIGN KEY (historical_project_summary_id) REFERENCES a2rp.historical_project_summary(historical_project_summary_id) ON DELETE CASCADE;


--
-- TOC entry 3535 (class 2606 OID 17903)
-- Name: historical_project_summary_resource historical_project_summary_resource_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.historical_project_summary_resource
    ADD CONSTRAINT historical_project_summary_resource_resource_fk FOREIGN KEY (resource_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3536 (class 2606 OID 17908)
-- Name: processing_order processing_order_processing_order_status_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_processing_order_status_fk FOREIGN KEY (processing_order_status_id) REFERENCES a2rp.processing_order_status(processing_order_status_id) ON DELETE CASCADE;


--
-- TOC entry 3537 (class 2606 OID 17913)
-- Name: processing_order processing_order_processing_order_type_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_processing_order_type_fk FOREIGN KEY (processing_order_type_id) REFERENCES a2rp.processing_order_type(processing_order_type_id) ON DELETE CASCADE;


--
-- TOC entry 3538 (class 2606 OID 17918)
-- Name: processing_order processing_order_project_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_project_fk FOREIGN KEY (project_id) REFERENCES a2rp.project(project_id) ON DELETE CASCADE;


--
-- TOC entry 3539 (class 2606 OID 17923)
-- Name: processing_order processing_order_resource_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_resource_2_fk FOREIGN KEY (project_manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3540 (class 2606 OID 17928)
-- Name: processing_order processing_order_resource_3_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_resource_3_fk FOREIGN KEY (value_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3541 (class 2606 OID 17933)
-- Name: processing_order processing_order_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_resource_fk FOREIGN KEY (program_manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3542 (class 2606 OID 17938)
-- Name: processing_order processing_order_task_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_task_fk FOREIGN KEY (task_id) REFERENCES a2rp.task(task_id) ON DELETE CASCADE;


--
-- TOC entry 3543 (class 2606 OID 17943)
-- Name: processing_order processing_order_technical_feature_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_technical_feature_fk FOREIGN KEY (technical_feature_id) REFERENCES a2rp.technical_feature(technical_feature_id) ON DELETE CASCADE;


--
-- TOC entry 3544 (class 2606 OID 17948)
-- Name: processing_order processing_order_work_breakdown_structure_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.processing_order
    ADD CONSTRAINT processing_order_work_breakdown_structure_fk FOREIGN KEY (work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3545 (class 2606 OID 17953)
-- Name: project project_customer_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_customer_fk FOREIGN KEY (customer_id) REFERENCES a2rp.customer(customer_id) ON DELETE CASCADE;


--
-- TOC entry 3546 (class 2606 OID 17958)
-- Name: project project_imputation_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_imputation_fk FOREIGN KEY (imputation_id) REFERENCES a2rp.imputation(imputation_id) ON DELETE CASCADE;


--
-- TOC entry 3547 (class 2606 OID 17963)
-- Name: project project_organizational_unit_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_organizational_unit_fk FOREIGN KEY (project_manager_organizational_unit_id) REFERENCES a2rp.organizational_unit(organizational_unit_id) ON DELETE CASCADE;


--
-- TOC entry 3548 (class 2606 OID 17968)
-- Name: project project_project_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_project_fk FOREIGN KEY (parent_id) REFERENCES a2rp.project(project_id) ON DELETE CASCADE;


--
-- TOC entry 3549 (class 2606 OID 17973)
-- Name: project project_project_status_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_project_status_fk FOREIGN KEY (project_status_id) REFERENCES a2rp.project_status(project_status_id) ON DELETE CASCADE;


--
-- TOC entry 3550 (class 2606 OID 17978)
-- Name: project project_project_type_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_project_type_fk FOREIGN KEY (project_type_id) REFERENCES a2rp.project_type(project_type_id) ON DELETE CASCADE;


--
-- TOC entry 3551 (class 2606 OID 17983)
-- Name: project project_resource_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_resource_2_fk FOREIGN KEY (owner_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3552 (class 2606 OID 17988)
-- Name: project project_resource_3_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_resource_3_fk FOREIGN KEY (program_manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3553 (class 2606 OID 17993)
-- Name: project project_resource_4_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_resource_4_fk FOREIGN KEY (project_manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3554 (class 2606 OID 17998)
-- Name: project project_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_resource_fk FOREIGN KEY (author_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3555 (class 2606 OID 18003)
-- Name: project project_work_breakdown_structure_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.project
    ADD CONSTRAINT project_work_breakdown_structure_fk FOREIGN KEY (work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3556 (class 2606 OID 18008)
-- Name: resource resource_cost_center_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_cost_center_2_fk FOREIGN KEY (cost_center_id) REFERENCES a2rp.cost_center(cost_center_id) ON DELETE CASCADE;


--
-- TOC entry 3557 (class 2606 OID 18013)
-- Name: resource resource_cost_center_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_cost_center_fk FOREIGN KEY (resource_cost_center_id) REFERENCES a2rp.cost_center(cost_center_id) ON DELETE CASCADE;


--
-- TOC entry 3558 (class 2606 OID 18018)
-- Name: resource resource_job_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_job_fk FOREIGN KEY (job_id) REFERENCES a2rp.job(job_id) ON DELETE CASCADE;


--
-- TOC entry 3559 (class 2606 OID 18023)
-- Name: resource resource_nt_account_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_nt_account_fk FOREIGN KEY (nt_account_id) REFERENCES a2rp.nt_account(nt_account_id) ON DELETE CASCADE;


--
-- TOC entry 3560 (class 2606 OID 18028)
-- Name: resource resource_organizational_unit_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_organizational_unit_2_fk FOREIGN KEY (resource_organizational_unit_id) REFERENCES a2rp.organizational_unit(organizational_unit_id) ON DELETE CASCADE;


--
-- TOC entry 3561 (class 2606 OID 18033)
-- Name: resource resource_organizational_unit_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_organizational_unit_fk FOREIGN KEY (organizational_unit_id) REFERENCES a2rp.organizational_unit(organizational_unit_id) ON DELETE CASCADE;


--
-- TOC entry 3562 (class 2606 OID 18038)
-- Name: resource resource_property_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_property_fk FOREIGN KEY (property_id) REFERENCES a2rp.property(property_id) ON DELETE CASCADE;


--
-- TOC entry 3563 (class 2606 OID 18043)
-- Name: resource resource_resource_breakdown_structure_1_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_breakdown_structure_1_fk FOREIGN KEY (resource_breakdown_structure_1_id) REFERENCES a2rp.resource_breakdown_structure(resource_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3564 (class 2606 OID 18048)
-- Name: resource resource_resource_breakdown_structure_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_breakdown_structure_2_fk FOREIGN KEY (resource_breakdown_structure_2_id) REFERENCES a2rp.resource_breakdown_structure(resource_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3565 (class 2606 OID 18053)
-- Name: resource resource_resource_breakdown_structure_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_breakdown_structure_fk FOREIGN KEY (resource_breakdown_structure_id) REFERENCES a2rp.resource_breakdown_structure(resource_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3566 (class 2606 OID 18058)
-- Name: resource resource_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_fk FOREIGN KEY (timesheet_manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3567 (class 2606 OID 18063)
-- Name: resource resource_resource_status_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_status_fk FOREIGN KEY (resource_status_id) REFERENCES a2rp.resource_status(resource_status_id) ON DELETE CASCADE;


--
-- TOC entry 3568 (class 2606 OID 18068)
-- Name: resource resource_resource_type_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.resource
    ADD CONSTRAINT resource_resource_type_fk FOREIGN KEY (resource_type_id) REFERENCES a2rp.resource_type(resource_type_id) ON DELETE CASCADE;


--
-- TOC entry 3569 (class 2606 OID 18073)
-- Name: task task_cost_center_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_cost_center_2_fk FOREIGN KEY (cost_center_id) REFERENCES a2rp.cost_center(cost_center_id) ON DELETE CASCADE;


--
-- TOC entry 3570 (class 2606 OID 18078)
-- Name: task task_cost_center_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_cost_center_fk FOREIGN KEY (executor_cost_center_id) REFERENCES a2rp.cost_center(cost_center_id) ON DELETE CASCADE;


--
-- TOC entry 3571 (class 2606 OID 18083)
-- Name: task task_organizational_unit_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_organizational_unit_fk FOREIGN KEY (organizational_unit_manager_id) REFERENCES a2rp.organizational_unit(organizational_unit_id) ON DELETE CASCADE;


--
-- TOC entry 3572 (class 2606 OID 18088)
-- Name: task task_processing_order_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_processing_order_fk FOREIGN KEY (processing_order_id) REFERENCES a2rp.processing_order(processing_order_id) ON DELETE CASCADE;


--
-- TOC entry 3573 (class 2606 OID 18093)
-- Name: task task_project_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_project_fk FOREIGN KEY (project_id) REFERENCES a2rp.project(project_id) ON DELETE CASCADE;


--
-- TOC entry 3574 (class 2606 OID 18098)
-- Name: task task_project_status_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_project_status_2_fk FOREIGN KEY (wp_status_id) REFERENCES a2rp.project_status(project_status_id) ON DELETE CASCADE;


--
-- TOC entry 3575 (class 2606 OID 18103)
-- Name: task task_project_status_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_project_status_fk FOREIGN KEY (project_status_id) REFERENCES a2rp.project_status(project_status_id) ON DELETE CASCADE;


--
-- TOC entry 3576 (class 2606 OID 18108)
-- Name: task task_resource_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_resource_fk FOREIGN KEY (manager_id) REFERENCES a2rp.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 3577 (class 2606 OID 18113)
-- Name: task task_task_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_task_fk FOREIGN KEY (parent_id) REFERENCES a2rp.task(task_id) ON DELETE CASCADE;


--
-- TOC entry 3578 (class 2606 OID 18118)
-- Name: task task_task_status_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_task_status_fk FOREIGN KEY (task_status_id) REFERENCES a2rp.task_status(task_status_id) ON DELETE CASCADE;


--
-- TOC entry 3579 (class 2606 OID 18123)
-- Name: task task_work_breakdown_structure_2_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_work_breakdown_structure_2_fk FOREIGN KEY (element_work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3580 (class 2606 OID 18128)
-- Name: task task_work_breakdown_structure_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.task
    ADD CONSTRAINT task_work_breakdown_structure_fk FOREIGN KEY (verify_work_breakdown_structure_id) REFERENCES a2rp.work_breakdown_structure(work_breakdown_structure_id) ON DELETE CASCADE;


--
-- TOC entry 3581 (class 2606 OID 18133)
-- Name: work_breakdown_structure work_breakdown_structure_project_fk; Type: FK CONSTRAINT; Schema: a2rp; Owner: postgres
--

ALTER TABLE ONLY a2rp.work_breakdown_structure
    ADD CONSTRAINT work_breakdown_structure_project_fk FOREIGN KEY (project_id) REFERENCES a2rp.project(project_id) ON DELETE CASCADE;


-- Completed on 2025-11-11 10:01:16

--
-- PostgreSQL database dump complete
--

\unrestrict jNkE1rdtGBoMYdHpe4XjxLyvPEQCBqKZ8GhAuMgGM7vwjGmTZn0IjcdsK094MY2

